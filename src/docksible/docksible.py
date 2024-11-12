import os
import argparse
from sys import path as sys_path
from getpass import getpass
from ansible_runner import Runner, RunnerConfig
from ansible_directory_helper.private_data import PrivateData

# Shouldn't need these.
import shlex
from subprocess import run, Popen, PIPE
from time import sleep

from docksible.constants import *
from docksible.arg_validator import ArgValidator

__author__ = "Brian St. Hilailre"
__copyright__ = "Copyright 2022, Sanctus Technologies UG (haftungsb.)"
__license__ = "Apache License, Version 2.0"
__version__ = "0.5.0"
__maintainer__ = "Brian St. Hilaire"
__email__ = "brian.st-hilaire@sanctus-tech.com"


def find_package_project_dir():
    for path_str in sys_path:
        try:
            try_path = os.path.join(path_str, 'docksible', 'project')
            assert os.path.isdir(try_path)
            return try_path
        except AssertionError:
            pass
    raise RuntimeError("Got no user supplied --project-dir, and could not find one in expected package location. Your Docksible installation is likely broken. However, if you are running this code directly from source, this is expected behavior. You probably forgot to pass the '--project-dir' flag. The directoy you're looking for is 'src/docksible/project/'.")


def get_pass_and_check(prompt, min_length):
    password = getpass(prompt)
    while len(password) < min_length:
        password = getpass('That password is too short. Please enter another password: ')
    double_check = getpass('Please retype password: ')
    if password == double_check:
        return password
    else:
        print('Passwords don\'t match. Please try again.')
        return get_pass_and_check(prompt, min_length)


def backup_dir(user, host, remote_dir, local_dest=DEFAULT_BACKUPS_DIR, delete=False):
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
    database_user,
    database_password,
    database_name,
    local_dest=DEFAULT_BACKUPS_DIR
):
    print("Starting database backup process...")
    proxy_process = proxy_connection(host, "docksible_db", 3306)

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
        database_user,
        database_password,
        database_name,
        local_dest=DEFAULT_BACKUPS_DIR,
        delete=False
):
    print("Started backup process...")
    if not os.path.exists(local_dest):
        os.makedirs(local_dest)
    backup_dir(user, host, "/root/docksible-volumes/ftp_data",
        local_dest, delete)
    backup_dir(user, host,
        "/root/docksible-volumes/wordpress_data/wp-content",
        local_dest, delete)
    backup_database(host, database_user, database_password,
        database_name, local_dest)
    print("Backup process finished.")


def proxy_connection(
    host,
    forwarded_host,
    remote_port,
    local_port=9000,
    proxy_user="proxy_user", 
    port=2222, 
):
    print("Opening proxy connection with following SSH-command:")
    ssh_command = "ssh -p {port} {proxy_user}@{host} \
        -L {local_port}:{forwarded_host}:{remote_port}".format(
            host=host,
            forwarded_host=forwarded_host,
            remote_port=remote_port,
            local_port=local_port,
            proxy_user=proxy_user,
            port=port,
        )
    print(ssh_command)
    try:
        return Popen(shlex.split(ssh_command), stdin=PIPE, stdout=PIPE,
            stderr=PIPE)
    except Exception as e:
        return e
    

def main():

    parser = argparse.ArgumentParser(
        prog='docksible',
        epilog='Work in progress...'
    )

    parser.add_argument('user', help="The user as whom you \
        (or rather, Ansible) will SSH into the server. For example: \
        root, azureuser, etc.")
    parser.add_argument('host', help="The server on which you deploy \
        your web service. For example: 123.123.123.123 or example.com")
    parser.add_argument('action', choices=[
        'setup-docker-compose',
        'redmine',
        'wordpress',
        'backup',
    ])

    parser.add_argument('--ask-remote-sudo', action='store_true')
    parser.add_argument('--insecure-cli-password', action='store_true')
    parser.add_argument('--remote-sudo-password')
    parser.add_argument('--database-root-password')
    parser.add_argument('--database-username')
    parser.add_argument('--database-password')
    parser.add_argument('--database-name')
    parser.add_argument('--database-table-prefix')
    parser.add_argument('--letsencrypt', '-l', action='store_true')
    parser.add_argument('--domain', '-d')
    parser.add_argument('--email',  '-e')
    parser.add_argument('--test-cert', '-t', action='store_true')
    parser.add_argument('--version', '-V', action='version', version=__version__)

    args = parser.parse_args()

    validator = ArgValidator(args)
    if validator.validate_args() != 0:
        print('FATAL! Bad args')
        return 1
    args = validator.get_args()


    private_data_dir = DEFAULT_PRIVATE_DATA_DIR
    project_dir = find_package_project_dir()

    private_data_obj = PrivateData(private_data_dir)

    private_data_obj.add_inventory_groups([
        'all',
    ])
    private_data_obj.add_inventory_host(args.host, 'all')
    private_data_obj.set_inventory_ansible_user(args.host, args.user)
    private_data_obj.write_inventory()

    # TODO: Improve this validation - this is just rudimentary.
    # if args.action == 'redmine':
    #     database_root_password = get_pass_and_check(
    #         'Please enter a database root password',
    #         7
    #     )
    # else:
    #     database_root_password = None

    # TODO: Temporary solution, do this better in the future.
    if args.action in ['backup']:
        do_backup(
            args.user,
            args.host,
            args.database_username,
            args.database_password,
            args.database_name,
            DEFAULT_BACKUPS_DIR
        )
    else:
        playbook = '{}.yml'.format(args.action)

        extravars = {
            'database_root_password': args.database_root_password,
            'database_username': args.database_username,
            'database_password': args.database_password,
            'database_name': args.database_name,
            # TODO: Don't need this anymore because now we fixed the antipattern
            # so we can just use 'ansible_host' in our playbook?
            # 'server_name': args.host,
        }

        if args.action == 'wordpress':
            extravars['wordpress_auth_vars'] = validator.get_wordpress_auth_vars()

        rc = RunnerConfig(
            private_data_dir=private_data_dir,
            project_dir=project_dir,
            # TODO: Improve this.
            playbook=playbook,
            extravars=extravars
        )

        rc.prepare()
        r = Runner(config=rc)
        r.run()

    if args.letsencrypt:

        # TODO: Validation...
        if args.domain is None:
            args.domain = args.host

        while args.email is None:
            args.email = input('Please enter an email address: ')

        # TODO: This is very rudimentary! In the future, we shouldn't
        # need to run a second play for this. Instead, do it all in one go.

        if args.action == 'redmine':
            port_to_encrypt = '3000'
        else:
            port_to_encrypt = '80'

        rc = RunnerConfig(
            private_data_dir=private_data_dir,
            project_dir=project_dir,
            # TODO: Improve this.
            playbook='letsencrypt.yml',
            extravars={
                'domain': args.domain,
                'email':  args.email,
                'service_to_encrypt': args.action,
                'port_to_encrypt':    port_to_encrypt,
                'test_cert': '--test-cert' if args.test_cert else ' ',
            }
        )

        rc.prepare()
        r = Runner(config=rc)
        r.run()

    private_data_obj.cleanup_dir()

    return 0


if __name__ == "__main__":
    main()
