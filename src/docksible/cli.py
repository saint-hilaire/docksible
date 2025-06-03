import argparse
from .constants import *
from .arg_validator import ArgValidator
from .docksible import Docksible

__author__ = "Brian St. Hilailre"
__copyright__ = "Copyright 2024 - 2025, Sanctus Technologies UG (haftungsb.)"
__license__ = "Apache License, Version 2.0"
__version__ = "1.0.0-dev"
__maintainer__ = "Brian St. Hilaire"
__email__ = "brian.st-hilaire@sanctus-tech.com"


def main():

    parser = argparse.ArgumentParser(
        prog='docksible'
    )

    parser.add_argument('user_at_host',
        help="""
        user and host where you want to \
        install your app. example: user@example.com, root@192.168.0.2, etc.
        If running locally, you can omit the user and simply pass in
        localhost, 127.0.0.1, etc.
        """
        )
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
    parser.add_argument('--database-table-prefix', default=DEFAULT_DATABASE_TABLE_PREFIX)
    parser.add_argument('--letsencrypt', '-l', action='store_true')
    parser.add_argument('--domain', '-d')
    parser.add_argument('--email',  '-e')
    parser.add_argument('--test-cert', '-t', action='store_true')
    parser.add_argument('--ssh-proxy', action='store_true',
        help="""
        Pass this flag to include a lightweight SSH proxy container
        in your Docker network, so you can port forward hidden services
        such as the database.
        """
    )
    parser.add_argument('--apparmor-workaround', action='store_true')
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
        sudo_password=args.remote_sudo_password,
        ssh_proxy=args.ssh_proxy,
        apparmor_workaround=args.apparmor_workaround,
    )

    if args.action == 'wordpress':
        docksible.wordpress_auth_vars = get_wordpress_auth_vars()

    # TODO: Temporary solution, do this better in the future.
    if args.action in ['backup']:
        raise NotImplementedError
    else:
        docksible.letsencrypt = args.letsencrypt
        docksible.domain = args.domain
        docksible.email = args.email
        docksible.test_cert = args.test_cert
        return docksible.run()


if __name__ == "__main__":
    main()
