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

home = os.environ['HOME']
ansible_playbook_path = home+"/ansible-playbooks/docker_ubuntu1804"
ansible_hosts_file_path = ansible_playbook_path+"/hosts"
dawn_path = home+"/dawn"
    
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

# TODO: Do this with a domain
def do_services(user, host, db_root_passwd, db_user, db_passwd, db_name):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")

    ansible_cmd = 'ansible-playbook -u {user} -i hosts playbook.yml --extra-vars "db_root_passwd={db_root_passwd} db_user={db_user} db_passwd={db_passwd} db_name={db_name}"'.format(user=user, db_root_passwd=db_root_passwd, db_user=db_user, db_passwd=db_passwd, db_name=db_name)
    os.system(ansible_cmd)
    os.system("git restore hosts")
    
def do_ssl_selfsigned(user, host, service_to_encrypt, port_to_encrypt):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")
    ansible_cmd = 'ansible-playbook -u {user} -i hosts --extra-vars "service_to_encrypt={service_to_encrypt} port_to_encrypt={port_to_encrypt}" ssl-selfsigned.yml'.format(user=user, service_to_encrypt=service_to_encrypt, port_to_encrypt=port_to_encrypt)
    os.system(ansible_cmd)
    os.system("git restore hosts")

def do_letsencrypt(user, host, domain, email, service_to_encrypt="wordpress", port_to_encrypt="80"):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")
    ansible_cmd = 'ansible-playbook -u {user} -i hosts --extra-vars "domain={domain} email={email} service_to_encrypt={service_to_encrypt} port_to_encrypt={port_to_encrypt}" letsencrypt.yml'.format(user=user, domain=domain, email=email, service_to_encrypt=service_to_encrypt, port_to_encrypt=port_to_encrypt)
    os.system(ansible_cmd)
    os.system("git restore hosts")

def do_redmine(user, host, database_root_password):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")
    ansible_cmd = 'ansible-playbook -u {user} -i hosts --extra-vars "database_root_password={database_root_password}" redmine.yml'.format(user=user, database_root_password=database_root_password)
    os.system(ansible_cmd)
    os.system("git restore hosts")

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

    parser.add_argument("-d", "--domain" )
    parser.add_argument("-e", "--email" )

    parser.add_argument("--service-to-encrypt", default="wordpress")
    parser.add_argument("--port-to-encrypt", default="80")

    # TODO: This is not currently compatible with the rest of the
    #       project.
    #       We are just doing this to be able to quickly set up a Redmine instance.
    #       Currently, it should just be passed together with the --bootstrap,-b flag.
    #       Ideally, we would want to integrate it together with the rest
    #       of the services.
    parser.add_argument("-R", "--redmine", action="store_true" )

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

    domain = args.domain
    email = args.email

    service_to_encrypt = args.service_to_encrypt
    port_to_encrypt = args.port_to_encrypt

    redmine = args.redmine

    if not (bootstrap or services or ssl_selfsigned or letsencrypt or redmine):
        exit("Please specify an action (--bootstrap, --services, --ssl-selfsigned and/or --letsencrypt)")

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
    if redmine:
        do_redmine(user, host, database_root_password)
    if ssl_selfsigned:
        do_ssl_selfsigned(user, host, service_to_encrypt, port_to_encrypt)
    if letsencrypt:
        do_letsencrypt(user, host, domain, email, service_to_encrypt, port_to_encrypt)

if __name__ == "__main__":
    main()
