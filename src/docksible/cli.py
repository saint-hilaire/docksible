import os
import argparse
from getpass import getpass
from ansible_runner import Runner, RunnerConfig
from ansible_directory_helper.private_data import PrivateData

# Shouldn't need these.
import shlex
from subprocess import run, Popen, PIPE
from time import sleep

from .constants import *
from .arg_validator import ArgValidator
from .docksible import Docksible

__author__ = "Brian St. Hilailre"
__copyright__ = "Copyright 2024, Sanctus Technologies UG (haftungsb.)"
__license__ = "Apache License, Version 2.0"
__version__ = "0.6.0"
__maintainer__ = "Brian St. Hilaire"
__email__ = "brian.st-hilaire@sanctus-tech.com"


# TODO
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


# TODO
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


# TODO
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


# TODO
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
        prog='docksible'
    )

    parser.add_argument('user_at_host', help="user and host where you want to \
        install your app. example: user@example.com, root@192.168.0.2, etc.")
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
    parser.add_argument('--private-data-dir', default=DEFAULT_PRIVATE_DATA_DIR)
    parser.add_argument('--version', '-V', action='version', version=__version__)

    args = parser.parse_args()

    validator = ArgValidator(args)
    if validator.validate_args() != 0:
        print('FATAL! Bad args')
        return 1

    args = validator.get_validated_args()

    docksible = Docksible(
        user=args.user,
        host=args.host,
        action=args.action,
        private_data_dir=args.private_data_dir,
        database_root_password=args.database_root_password,
        database_username=args.database_username,
        database_password=args.database_password,
        database_name=args.database_name,
    )

    if args.action == 'wordpress':
        docksible.wordpress_auth_vars = get_wordpress_auth_vars()

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
        docksible.set_playbook('{}.yml'.format(args.action))
        docksible.letsencrypt = args.letsencrypt
        docksible.domain = args.domain
        docksible.email = args.email
        docksible.test_cert = args.test_cert
        docksible.run()

    return 0


if __name__ == "__main__":
    main()
