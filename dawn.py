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
        replace_line_in_file(ansible_hosts_file_path, "123.123.123.123",
            host + "    ansible_python_interpreter=/usr/bin/python3")
    except:
        exit("Could not find an Ansible hosts file! Exiting.")

    # This installs Docker and Docker Compose.
    os.chdir(ansible_playbook_path)
    os.system("ansible-playbook -u " + user + " -i hosts playbook.yml")

    # This sets the host's IP address back to the placeholder,
    # so that it gets caught next time (if the host should change)
    os.system("git restore hosts")

def do_services(user, host, db_root_passwd, db_user, db_passwd, db_name):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", 
        host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")

    ansible_cmd = 'ansible-playbook -u {user} -i hosts playbook.yml \
        --extra-vars "db_root_passwd={db_root_passwd} \
        db_user={db_user} db_passwd={db_passwd} db_name={db_name}"'.format(
            user=user,
            db_root_passwd=db_root_passwd,
            db_user=db_user,
            db_passwd=db_passwd,
            db_name=db_name
        )
    os.system(ansible_cmd)
    os.system("git restore hosts")
    

# TODO: After deploying a Django app with this, you have to restart its 
# Docker container. Otherwise, navigating to other pages throws error 500.
# It seems that the database migration fails to run, but restarting the
# container fixes that.
def do_custom_service(
    user,
    host,
    domain,
    database_root_password,
    database_user,
    database_password,
    database_name,
    service_name,
    app_name,
    # TODO: The playbook also needs to SSH-keyscan the webservice
    # (i.e. GitHub), where the repo is hosted, so that the playbook can clone
    # the repository. Possibly also need to load a user's SSH key, if the repo
    # is private. Otherwise, the user needs to do this manually.
    django_app_repository,
    django_app_git_branch,
    django_dockerfile_path,
):
    if app_name != "":
        app_name_extravar = "app_name="+app_name
    else:
        app_name_extravar = ""
    if domain == "" or domain is None:
        domain = host
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123",
        host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")
    ansible_cmd = 'ansible-playbook -u {user} -i hosts --extra-vars \
        "database_root_password={database_root_password} \
        database_user={database_user} database_password={database_password} \
        database_name={database_name} \
        service_name={service_name} {app_name_extravar} \
        domain={domain} \
        django_app_repository={django_app_repository} \
        django_app_git_branch={django_app_git_branch} \
        django_dockerfile_path={django_dockerfile_path}" \
        {service_name}.yml'.format( # TODO: Figure out how to do this
                                    # conditionally in Ansible.
            user=user,
            domain=domain,
            database_root_password=database_root_password,
            database_user=database_user,
            database_password=database_password,
            database_name=database_name,
            service_name=service_name,
            app_name_extravar=app_name_extravar,
            django_app_repository=django_app_repository,
            django_app_git_branch=django_app_git_branch,
            django_dockerfile_path=django_dockerfile_path,
    )
    os.system(ansible_cmd)
    os.system("git restore hosts")


def do_ssl_selfsigned(user, host, service_to_encrypt, port_to_encrypt):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123",
        host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")
    ansible_cmd = 'ansible-playbook -u {user} -i hosts --extra-vars \
        "service_to_encrypt={service_to_encrypt} \
        port_to_encrypt={port_to_encrypt}" ssl-selfsigned.yml'.format(
            user=user,
            service_to_encrypt=service_to_encrypt,
            port_to_encrypt=port_to_encrypt
        )
    os.system(ansible_cmd)
    os.system("git restore hosts")

def do_letsencrypt(
    user,
    host,
    domain,
    email,
    service_to_encrypt="wordpress",
    port_to_encrypt="80",
    test_cert=False,
    app_name=""
):
    if test_cert:
        test_cert = "--test-cert"
    else:
        test_cert = " "
    if app_name != "":
        app_name_extravar = " app_name="+app_name
    else:
        app_name_extravar = " "

    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", 
        host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")
    ansible_cmd = 'ansible-playbook -u {user} -i hosts \
        --extra-vars "domain={domain} email={email} \
        service_to_encrypt={service_to_encrypt} \
        port_to_encrypt={port_to_encrypt} test_cert={test_cert} \
        {app_name_extravar}" \
        letsencrypt.yml'.format(
            user=user, 
            domain=domain,
            email=email,
            service_to_encrypt=service_to_encrypt,
            port_to_encrypt=port_to_encrypt,
            test_cert=test_cert,
            app_name_extravar=app_name_extravar
        )
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

def backup_database(
    host,
    path_to_ssh_key,
    database_user,
    database_password,
    database_name,
    local_dest=backups_path
):
    print("Starting database backup process...")
    proxy_process = proxy_connection(host, "dawn_db", 3306, path_to_ssh_key)

    # TODO: Test database connectivity, and don't go on until it is OK.
    #       But for now, 7 seconds seems enough
    #       to build up the tunnel connection.
    sleep(7)
    mysql_dump_output_file = open("{local_dest}/{database_name}.sql".format(
        local_dest=local_dest,
        database_name=database_name
        ), "w")
    mysql_dump_cmd = "mysqldump --user={database_user} \
        --password={database_password} --port=9000 --host=127.0.0.1 \
        --protocol=TCP --no-tablespaces --column-statistics=0 \
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

def do_backup(
        user,
        host,
        path_to_ssh_key,
        database_user,
        database_password,
        database_name,
        local_dest=backups_path,
        delete=False
):
    print("Started backup process...")
    backup_dir(user, host, "/root/dawn_docker_volumes/ftp_data",
        local_dest, delete)
    backup_dir(user, host,
        "/root/dawn_docker_volumes/wordpress_data/wp-content",
        local_dest, delete)
    backup_database(host, path_to_ssh_key, database_user, database_password,
        database_name, local_dest)
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
        return Popen(shlex.split(ssh_command), stdin=PIPE, stdout=PIPE,
            stderr=PIPE)
    except Exception as e:
        return e
    
    

def main():
    os.chdir(home)

    if not os.path.isfile(
        home+"/ansible-playbooks/docker_ubuntu1804/playbook.yml"
    ):
        os.system("git clone https://github.com/sanctus91/ansible-playbooks.git")


    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host" )
    parser.add_argument("-U", "--user" )

    parser.add_argument("-P", "--database-root-password",
        default="db_root_password")
    parser.add_argument("-u", "--database-user", default="db_user")
    parser.add_argument("-p", "--database-password",
        default="db_password")
    parser.add_argument("-D", "--database-name", default="db_name")
    parser.add_argument("-b", "--bootstrap", action="store_true")
    parser.add_argument("-s", "--services", action="store_true")
    parser.add_argument("-S", "--ssl-selfsigned", action="store_true")
    # TODO: We should think about what we really want to do here.
    #       When I first started this project, I mainly had WordPress in mind,
    #       so that is 'baked in' together with the --services flag.
    #       Then Redmine entered the picture and it was then the
    #       -R, --redmine flag, and now that I need a Django installation, I
    #       am changing it again, to -C, --custom-service.
    #
    #       It would be cool if we could specify something like --wordpress,
    #       --redmine, --django, --irc, etc., but that would require some
    #       serious wrangling of docker-compose files, which would all be
    #       rather clunky. It would also be reinventing the PaaS wheel.
    #
    #       For the scope of this project, perhaps just implement some
    #       ready-to-go, prepackaged environments, WordPress, Django and
    #       Redmine being good examples. Other stuff, like IRC or FTP may or
    #       may not be hard coded, depending on what I want to do. To truly be
    #       able to customize your cloud services would likely be beyond the
    #       scope of this project, you'd need a real PaaS project for that.
    parser.add_argument("-C", "--custom-service", action="store_true")
    parser.add_argument("-n", "--service-name")
    parser.add_argument("-a", "--app-name", default="")
    parser.add_argument("-R", "--django-app-repository", default="")
    parser.add_argument("-g", "--django-app-git-branch", default="production")
    parser.add_argument("-j", "--django-dockerfile-path", default="Dockerfile")
    parser.add_argument("-l", "--letsencrypt", action="store_true")
    parser.add_argument("-t", "--test-cert", action="store_true")
    parser.add_argument("-B", "--backup", action="store_true")
    parser.add_argument("-E", "--delete-in-rsync", action="store_true")
    parser.add_argument("-i", "--path-to-ssh-key", default=home+"/.ssh/id_rsa")
    parser.add_argument("-L", "--local-backup-dest", default=backups_path)

    parser.add_argument("-d", "--domain", default="")
    parser.add_argument("-e", "--email")

    parser.add_argument("--service-to-encrypt", default="wordpress")
    parser.add_argument("--port-to-encrypt", default="80")


    args = parser.parse_args()

    host = args.host
    user = args.user

    database_root_password = args.database_root_password
    database_user = args.database_user
    database_password = args.database_password
    database_name = args.database_name
    bootstrap = args.bootstrap
    services = args.services
    custom_service = args.custom_service
    service_name = args.service_name
    app_name = args.app_name
    django_app_repository = args.django_app_repository
    django_app_git_branch = args.django_app_git_branch
    django_dockerfile_path = args.django_dockerfile_path
    ssl_selfsigned = args.ssl_selfsigned
    letsencrypt = args.letsencrypt
    test_cert = args.test_cert
    backup = args.backup
    delete_in_rsync = args.delete_in_rsync
    path_to_ssh_key = args.path_to_ssh_key
    local_backup_dest = args.local_backup_dest

    domain = args.domain
    email = args.email

    service_to_encrypt = args.service_to_encrypt
    port_to_encrypt = args.port_to_encrypt


    if not (bootstrap or services or ssl_selfsigned or letsencrypt or 
        custom_service or backup
    ):
        exit("Please specify an action (--bootstrap, --services, \
            --custom-service, --ssl-selfsigned and/or --letsencrypt)")

    # Checking for required arguments
    if host is None or user is None:
        exit("Please specify a host and a user.")

    if database_root_password == "db_root_password":
        print("WARNING! Using default value for database root password: \
            'db_root_password'! This is unsafe in production environments!")
    if database_user == "db_user":
        print("WARNING! Using default value for database user: 'db_user'! \
            This is unsafe in production environments!")
    if database_password == "db_password":
        print("WARNING! Using default value for database password: \
            'db_password'! This is unsafe in production environments!")
    if database_name == "db_name":
        print("WARNING! Using default value for database name: 'db_name'! \
            This is unsafe in production environments!")

    if custom_service and service_name is None:
        exit("Please specify a service name (--service-name[redmine|django])")
    elif service_name == "django" and \
        (app_name == "" or django_app_repository == ""):
        exit("Please specify a name and repository for your Django app with \
            the --app-name --django-app-repository flags")

    if bootstrap:
        do_bootstrap(user, host)
    if services:
        do_services(
            user,
            host,
            database_root_password,
            database_user,
            database_password,
            database_name
        )
    if custom_service:
        do_custom_service(
            user,
            host,
            domain,
            database_root_password,
            database_user,
            database_password,
            database_name,
            service_name,
            app_name,
            django_app_repository,
            django_app_git_branch,
            django_dockerfile_path,
        )
    if ssl_selfsigned:
        do_ssl_selfsigned(user, host, service_to_encrypt, port_to_encrypt)
    if letsencrypt:
        do_letsencrypt(
            user,
            host,
            domain,
            email,
            service_to_encrypt,
            port_to_encrypt,
            test_cert,
            app_name
        )
    if backup:
        do_backup(
            user,
            host,
            path_to_ssh_key,
            database_user,
            database_password,
            database_name,
            local_backup_dest,
            delete_in_rsync
        )

if __name__ == "__main__":
    main()
