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

def services(user, host):
    replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    os.chdir(dawn_path+"/ansible")
    os.system("ansible-playbook -u " + user + " -i hosts playbook.yml")
    os.system("git restore hosts")
    


def main():
    os.chdir(home)

    if not os.path.isfile(home+"/ansible-playbooks/docker_ubuntu1804/playbook.yml"):
        os.system("git clone https://github.com/sanctus91/ansible-playbooks.git")


    parser = argparse.ArgumentParser()
    parser.add_argument("-H", "--host" )
    parser.add_argument("-u", "--user" )
    args = parser.parse_args()

    host = args.host
    user = args.user

    if host is None or user is None:
        exit("Please specify a host and a user.")

    try:
        replace_line_in_file(ansible_hosts_file_path, "123.123.123.123", host + "    ansible_python_interpreter=/usr/bin/python3")
    except:
        exit("Could not find an Ansible hosts file! Exiting.")

    # This does the actual deployment.
    os.chdir(ansible_playbook_path)
    os.system("ansible-playbook -u " + user + " -i hosts playbook.yml")

    # This sets the host's IP address back to the placeholder, so that it gets caught next time (if the host should change)
    os.system("git restore hosts")

    services(user, host)

if __name__ == "__main__":
    main()
