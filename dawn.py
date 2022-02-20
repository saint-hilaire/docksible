#!/usr/bin/env python3
"""
Run this script on a local machine, to deploy all the resources
required by your website.

Requirements:
    Local:
        - Python3
        - Git
        - Ansible
    On the server:
        - A VPS with all the ports open that you require. These are recommended:
            - "The usual" 22, 80, 443.
            - 2222 for the SSH-proxy
        - SSH-access
"""

import os
import argparse
import shlex
from subprocess import run, Popen, PIPE
from time import sleep

home = os.environ['HOME']
ansible_playbook_path = home+"/ansible-playbooks/docker_ubuntu1804"
ansible_hosts_file_path = ansible_playbook_path+"/hosts"
dawn_path = home+"/dawn"
backups_path = home+"/backups"
    
def replace_line_in_file(file_path, search_for, replace_with):
    with open(file_path, "r") as file_handle:
        lines = file_handle.readlines()
    with open(file_path, "w") as file_handle:
        for line in lines:
            if search_for in line:
                file_handle.write(replace_with)
            else:
                file_handle.write(line)


def do_bootstrap(user, host):
    try:
        replace_line_in_file(ansible_hosts_file_path, "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    except:
        exit("Could not find an Ansible hosts file! Exiting.")

    # This installs Docker and Docker Compose.
    os.chdir(ansible_playbook_path)
    os.system("ansible-playbook -u " + user + " -i hosts playbook.yml")

    # This sets the host's IP address back to the placeholder, so that it gets caught next time (if the host should change)
    os.system("git restore hosts")

def do_services(user, host, db_root_passwd, db_user, db_passwd, db_name):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")

    ansible_cmd = 'ansible-playbook -u {user} -i hosts playbook.yml --extra-vars "db_root_passwd={db_root_passwd} db_user={db_user} db_passwd={db_passwd} db_name={db_name}"'.format(user=user, db_root_passwd=db_root_passwd, db_user=db_user, db_passwd=db_passwd, db_name=db_name)
    os.system(ansible_cmd)
    os.system("git restore hosts")
    
def do_ssl_selfsigned(user, host):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")
    ansible_cmd = 'ansible-playbook -u {user} -i hosts ssl-selfsigned.yml'.format(user=user)
    os.system(ansible_cmd)
    os.system("git restore hosts")

def do_letsencrypt(user, host, domain, email):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")
    ansible_cmd = 'ansible-playbook -u {user} -i hosts --extra-vars "domain={domain} email={email}" letsencrypt.yml'.format(user=user, domain=domain, email=email)
    os.system(ansible_cmd)
    os.system("git restore hosts")

def backup_dir(user, host, remote_dir, local_dest=backups_path, delete=False):
    print("Backing up {remote_dir}...".format(remote_dir=remote_dir))
    rsync_cmd = "rsync --recursive --no-links "
    if delete:
        rsync_cmd += "--delete "
    rsync_cmd += "{user}@{host}:{remote_dir} {local_dest}/".format(
        user=user,
        host=host,
        remote_dir=remote_dir,
        local_dest=local_dest
    )
    proc = run(shlex.split(rsync_cmd))
    print("... Done.")

def backup_database(host, path_to_ssh_key, database_user, database_password, database_name, local_dest=backups_path):
    print("Starting database backup process...")
    proxy_process = proxy_connection(host, "dawn_db", 3306, path_to_ssh_key)

    # TODO: Test database connectivity, and don't go on until it is OK.
    #       But for now, 7 seconds seems enough to build up the tunnel connection.
    sleep(7)
    mysql_dump_output_file = open("{local_dest}/{database_name}.sql".format(
        local_dest=local_dest,
        database_name=database_name
        ), "w")
    mysql_dump_cmd = "mysqldump --user={database_user} --password={database_password} \
        --port=9000 --host=127.0.0.1 --protocol=TCP --no-tablespaces --column-statistics=0 \
        {database_name}".format(
            database_user=database_user,
            database_password=database_password,
            database_name=database_name,
        )
    print("Starting mysqldump...")
    print(mysql_dump_cmd)
    proc = run(shlex.split(mysql_dump_cmd), stdout=mysql_dump_output_file)
    print("... Done.")

    print("Killing proxy connection...")
    proxy_process.kill()
    print("... Done.")
    mysql_dump_output_file.close()

def do_backup(user, host, path_to_ssh_key, database_user, database_password, database_name, local_dest=backups_path, delete=False):
    print("Started backup process...")
    backup_dir(user, host, "/root/dawn_docker_volumes/ftp_data", local_dest, delete)
    backup_dir(user, host, "/root/dawn_docker_volumes/wordpress_data/wp-content", local_dest, delete)
    backup_database(host, path_to_ssh_key, database_user, database_password, database_name, local_dest)
    print("Backup process finished.")

def proxy_connection(
    host,
    forwarded_host,
    remote_port,
    path_to_ssh_key="~/.ssh/id_rsa", 
    local_port=9000,
    proxy_user="proxy_user", 
    port=2222, 
    ):
    print("Opening proxy connection with following SSH-command:")
    ssh_command = "ssh -p {port} -i {path_to_ssh_key} {proxy_user}@{host} \
        -L {local_port}:{forwarded_host}:{remote_port}".format(
            host=host,
            forwarded_host=forwarded_host,
            remote_port=remote_port,
            local_port=local_port,
            proxy_user=proxy_user,
            port=port,
            path_to_ssh_key=path_to_ssh_key
        ) 
    print(ssh_command)
    try:
        return Popen(shlex.split(ssh_command), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    except Exception as e:
        return e
    
    

def main():
    os.chdir(home)

    if not os.path.isfile(home+"/ansible-playbooks/docker_ubuntu1804/playbook.yml"):
        os.system("git clone https://github.com/sanctus91/ansible-playbooks.git")


    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host" )
    parser.add_argument("-u", "--user" )

    parser.add_argument("-P", "--database-root-password", default="root_password" )
    parser.add_argument("-U", "--database-user", default="wordpress" )
    parser.add_argument("-p", "--database-password", default="wordpress_password" )
    parser.add_argument("-D", "--database-name", default="wordpress" )
    parser.add_argument("-b", "--bootstrap", action="store_true" )
    parser.add_argument("-s", "--services", action="store_true" )
    parser.add_argument("-S", "--ssl-selfsigned", action="store_true" )
    parser.add_argument("-l", "--letsencrypt", action="store_true" )
    parser.add_argument("-B", "--backup", action="store_true" )
    parser.add_argument("-E", "--delete-in-rsync", action="store_true" )
    parser.add_argument("-i", "--path-to-ssh-key", default=home+"/.ssh/id_rsa" )
    parser.add_argument("-L", "--local-backup-dest", default=backups_path )

    parser.add_argument("-d", "--domain" )
    parser.add_argument("-e", "--email" )

    args = parser.parse_args()

    host = args.host
    user = args.user

    database_root_password = args.database_root_password
    database_user = args.database_user
    database_password = args.database_password
    database_name = args.database_name
    bootstrap = args.bootstrap
    services = args.services
    ssl_selfsigned = args.ssl_selfsigned
    letsencrypt = args.letsencrypt
    backup = args.backup
    delete_in_rsync = args.delete_in_rsync
    path_to_ssh_key = args.path_to_ssh_key
    local_backup_dest = args.local_backup_dest

    domain = args.domain
    email = args.email

    if not (bootstrap or services or ssl_selfsigned or letsencrypt or backup):
        exit("Please specify an action (--bootstrap, --services, --ssl-selfsigned, --letsencrypt, and/or --backup)")

    # Checking for required arguments
    if host is None or user is None:
        exit("Please specify a host and a user.")

    if database_root_password == "root_password":
        print("WARNING! Using default value for database root password: 'root_password'! This is unsafe in production environments!")
    if database_user == "wordpress":
        print("WARNING! Using default value for database user: 'wordpress'! This is unsafe in production environments!")
    if database_password == "wordpress_password":
        print("WARNING! Using default value for database password: 'wordpress_password'! This is unsafe in production environments!")
    if database_name == "wordpress":
        print("WARNING! Using default value for database name: 'wordpress'! This is unsafe in production environments!")


    if bootstrap:
        do_bootstrap(user, host)
    if services:
        do_services(user, host, database_root_password, database_user, database_password, database_name)
    if ssl_selfsigned:
        do_ssl_selfsigned(user, host)
    if letsencrypt:
        do_letsencrypt(user, host, domain, email)
    if backup:
        do_backup(user, host, path_to_ssh_key, database_user, database_password, database_name, local_backup_dest, delete_in_rsync)

if __name__ == "__main__":
    main()
