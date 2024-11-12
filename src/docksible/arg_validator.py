from re import match
from copy import copy
from warnings import warn
from getpass import getpass
from fqdn import FQDN
from docksible.constants import *

INSECURE_CLI_PASS_WARNING = 'It\'s insecure to pass passwords via CLI args! If you are sure that you want to do this, rerun this command with the --insecure-cli-password flag.'

class ArgValidator():

    def __init__(self, args):
        self.raw_args       = args
        self.validated_args = args


    def get_raw_args(self):
        return self.raw_args


    def get_validated_args(self):
        return self.validated_args


    # TODO?
    def handle_defaults(
        self,
        default_args,
        ask_user=False,
        verbose=False
    ):
        """Handles defaults in various cases, optionally setting values with
        application wide defaults or overriding values, and optionally
        printing warnings.

        Positional arguments

        default_args -- A list of dictionaries, which defines the arguments,
                        and how to treat them. The following dictionary serves
                        as an example:
            {
                # required
                'arg_name': 'some_cli_arg', # The user passed this in as
                                            # --some-cli-arg - We also have a
                                            # helper function to get the arg
                                            # name in that format.
                # required
                'cli_default_value': DEFAULT_ARG_VALUE,
                # optional
                'override_default_value': 'some use case specific default',
            }

        ask_user -- Optional. If True, then if we got default values,
                    prompt the user to input their own value,
                    and if they leave it blank,
                    fall back to default values. Defaults to False.

        verbose --  Optional. If True, then if we are using some
                    default value, warn the user about this. This is useful
                    for credentials, in case we're falling back to some
                    insecure value.
        """
        for arg_dict in default_args:
            try:
                default_value = arg_dict['override_default_value']
            except KeyError:
                default_value = arg_dict['cli_default_value']
            user_value = getattr(self.raw_args, arg_dict['arg_name'])

            if user_value == arg_dict['cli_default_value']:
                if ask_user:
                    tmp_val = input(
                        'Got no {}. Please enter a value now, or leave blank to default to \'{}\': '.format(

                            self.var_name_to_cli_arg(arg_dict['arg_name']),
                            default_value
                        )
                    )
                    if tmp_val == '':
                        tmp_val = default_value
                    default_value = tmp_val

                setattr(
                    self.validated_args,
                    arg_dict['arg_name'],
                    default_value
                )

                if verbose:
                    print('Using {} value \'{}\'.'.format(
                        self.var_name_to_cli_arg(arg_dict['arg_name']),
                        default_value
                    ))


    def var_name_to_cli_arg(self, var_name):
        return '--{}'.format(var_name.replace('_', '-'))


    def get_pass_and_check(self, prompt, min_length=0, confirm=False):
        password = getpass(prompt)
        while min_length > 0 and len(password) < min_length:
            password = getpass('That password is too short. Please enter another password: ')
        if confirm:
            double_check = getpass('Please retype password: ')
            if password == double_check:
                return password
            else:
                print('Passwords don\'t match. Please try again.')
                return self.get_pass_and_check(prompt, min_length, True)
        else:
            return password


    def validate_ansible_runner_args(self):
        try:
            user_at_host_split = self.raw_args.user_at_host.split('@')
            assert len(user_at_host_split) == 2
            self.validated_args.user = user_at_host_split[0]
            self.validated_args.host = user_at_host_split[1]
        except AssertionError:
            print("FATAL! First positional argument must be in the format 'user@host'.")
            return 1
        if self.raw_args.remote_sudo_password \
            and not self.raw_args.insecure_cli_password:
            print(INSECURE_CLI_PASS_WARNING)
            return 1
        if self.raw_args.ask_remote_sudo:
            self.validated_args.remote_sudo_password = self.get_pass_and_check(
                'Please enter sudo password for remote host: ')
        return 0


    def validate_database_args(self):

        if not self.raw_args.insecure_cli_password \
            and (self.raw_args.database_password \
                or self.raw_args.database_root_password
            ):

            print(INSECURE_CLI_PASS_WARNING)
            return 1

        # TODO: Add some option like --wordpress-defaults, to improve user
        # experience. Otherwise, the user would always be asked about defaulting
        # to 'wordpress' and 'wp_' for database name and table prefix, which
        # might be a little annoying.
        if self.raw_args.action == 'wordpress':
            self.handle_defaults([
                {
                    'arg_name': 'database_name',
                    'cli_default_value': None,
                    'override_default_value': 'wordpress',
                },
                {
                    'arg_name': 'database_username',
                    'cli_default_value': None,
                    'override_default_value': DEFAULT_DATABASE_USERNAME,
                },
                {
                    'arg_name': 'database_table_prefix',
                    'cli_default_value': DEFAULT_DATABASE_TABLE_PREFIX,
                    'override_default_value': 'wp_',
                },
            ], True, True)

        if not self.raw_args.database_root_password:

            self.validated_args.database_root_password = self.get_pass_and_check(
                'Please enter a database root password: ',
                0,
                True
            )

        if self.raw_args.action == 'backup':
            self.handle_defaults([
                {
                    'arg_name': 'database_name',
                    'cli_default_value': None,
                    'override_default_value': DEFAULT_DATABASE_NAME,
                },
                {
                    'arg_name': 'database_username',
                    'cli_default_value': None,
                    'override_default_value': DEFAULT_DATABASE_USERNAME,
                },
            ], True, True)

        if self.raw_args.database_username and not self.raw_args.database_password:
            self.validated_args.database_password = self.get_pass_and_check(
                'Please enter a database password: ',
                0,
                True
            )

        return 0


    def validate_ssl_args(self):

        if not self.raw_args.letsencrypt:
            return 0

        if self.raw_args.domain is None:
            self.validated_args.domain = self.validated_args.host

        while self.validated_args.email is None \
                or not match(r"[^@]+@[^@]+\.[^@]+", self.validated_args.email
                ):
            self.validated_args.email = input('Please enter a valid email address: ')

        return 0


    def validate_args(self):
        validate_methods = [
            'validate_ansible_runner_args',
            'validate_database_args',
            'validate_ssl_args',
        ]
        for method_name in validate_methods:
            method = getattr(self, method_name)
            result = method()
            if result != 0:
                return result

        return 0
