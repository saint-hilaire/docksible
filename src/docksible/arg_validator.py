# TODO: This will need to be improved!
# I copy-pasted from another project, but I want to that stuff
# in a dedicated library - that's what the other comments
# about "The Library" are about.

from re import match
from copy import copy
from secrets import token_hex
from warnings import warn
from getpass import getpass
from fqdn import FQDN
from docksible.constants import *

INSECURE_CLI_PASS_WARNING = 'It\'s insecure to pass passwords via CLI args! If you are sure that you want to do this, rerun this command with the --insecure-cli-password flag.'

class ArgValidator():

    def __init__(self, args):
        self.args = args


    def get_args(self):
        return self.args


    # TODO?
    def get_wordpress_auth_vars(self):
        auth_var_names = [
            'auth_key',
            'secure_auth_key',
            'logged_in_key',
            'nonce_key',
            'auth_salt',
            'secure_auth_salt',
            'logged_in_salt',
            'nonce_salt',
        ]
        auth_vars = {}

        for var in auth_var_names:
            # must_generate = False
            # warn_user     = False

            # if not getattr(self.args, 'wordpress_{}'.format(var)):
            #     must_generate = True
            # elif len(getattr(self.args, 'wordpress_{}'.format(var))) < 32:
            #     must_generate = True
            #     warn_user     = True

            # if must_generate:
            #     auth_vars[var.upper()] = token_hex(64)
            # else:
            #     auth_vars[var.upper()] = getattr(
            #         self.args,
            #         'wordpress_{}'.format(var)
            #     )

            # if warn_user:
            #     print('The value you passed for {} is too short! I will automatically generate a value for you, and use that. If in doubt, you should leave this argument blank, to use automatically generated values. See the file wp-config.php on your server.'.format(
            #         self.var_name_to_cli_arg('wordpress_{}'.format(var))
            #     ))

            # TODO: In the future, let the user optionally define these
            # values, using the old commented out code above from Lampsible,
            # which we shouldn't be copy-pasting around like this anyway,
            # but for now, always generate it automatically...
            auth_vars['WORDPRESS_{}'.format(var.upper())] = token_hex(64)


        return auth_vars


    # TODO?
    def get_certbot_domains_string(self):
        try:
            return '-d {}'.format(' -d '.join(self.args.domains_for_ssl))
        except TypeError:
            return ''


    # TODO?
    def get_certbot_test_cert_string(self):
        return '--test-cert' if self.args.test_cert else ''


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
            user_value = getattr(self.args, arg_dict['arg_name'])

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
                    self.args,
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
        if self.args.remote_sudo_password \
            and not self.args.insecure_cli_password:
            print(INSECURE_CLI_PASS_WARNING)
            return 1
        if self.args.ask_remote_sudo:
            self.args.remote_sudo_password = self.get_pass_and_check(
                'Please enter sudo password for remote host: ')
        return 0


    def validate_database_args(self):

        if not self.args.insecure_cli_password \
            and (self.args.database_password \
                or self.args.database_root_password
            ):

            print(INSECURE_CLI_PASS_WARNING)
            return 1

        # TODO: Add some option like --wordpress-defaults, to improve user
        # experience. Otherwise, the user would always be asked about defaulting
        # to 'wordpress' and 'wp_' for database name and table prefix, which
        # might be a little annoying.
        if self.args.action == 'wordpress':
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

        if not self.args.database_root_password:

            self.args.database_root_password = self.get_pass_and_check(
                'Please enter a database root password: ',
                0,
                True
            )

        if self.args.action == 'backup':
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

        if self.args.database_username and not self.args.database_password:
            self.args.database_password = self.get_pass_and_check(
                'Please enter a database password: ',
                0,
                True
            )

        return 0


    def validate_ssl_args(self):

        if self.args.ssl_certbot:
            ssl_action = 'certbot'
        elif self.args.ssl_selfsigned:
            ssl_action = 'selfsigned'
        else:
            ssl_action = None

        if ssl_action == 'certbot':
            self.handle_defaults([
                {
                    'arg_name': 'domains_for_ssl',
                    'cli_default_value': None,
                    'override_default_value': [self.args.host],
                },
                {
                    'arg_name': 'email_for_ssl',
                    'cli_default_value': None,
                    'override_default_value': self.args.apache_server_admin,
                },
            ])

            if not match(r"[^@]+@[^@]+\.[^@]+", self.args.email_for_ssl):
                print("FATAL! --email-for-ssl needs to be valid. Got '{}'. Aborting.".format(
                    self.args.email_for_ssl))
                return 1

            if self.args.action == 'wordpress':
                if self.args.host[:4] == 'www.':
                    www_domain = self.args.host
                else:
                    www_domain = 'www.{}'.format(self.args.host)

                if www_domain not in self.args.domains_for_ssl:
                    self.args.domains_for_ssl.append(www_domain)

                self.domain_for_wordpress = www_domain

        return 0


    def validate_args(self):
        validate_methods = [
            'validate_ansible_runner_args',
            'validate_database_args',
            # TODO?
            # 'validate_ssl_args',
        ]
        for method_name in validate_methods:
            method = getattr(self, method_name)
            result = method()
            if result != 0:
                return result

        return 0
