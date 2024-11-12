from ansible_runner import Runner, RunnerConfig
from ansible_directory_helper.private_data import PrivateData
from .constants import *


class Docksible:

    def __init__(self, user, host, action,
            private_data_dir=DEFAULT_PRIVATE_DATA_DIR,
            database_root_password=None, database_username=None,
            database_password=None, database_name=None,
            letsencrypt=False,
            wordpress_auth_vars=None,
            domain=None, email=None,
            test_cert=False
        ):
        self.user   = user
        self.host   = host
        self.action = action

        self.private_data_helper = PrivateData(private_data_dir)
        self._init_inventory()

        self.runner_config = RunnerConfig(
            private_data_dir=private_data_dir,
            project_dir=PROJECT_DIR
        )
        self.runner = Runner(self.runner_config)

        self.database_root_password = database_root_password
        self.database_username = database_username
        self.database_password = database_password
        self.database_name = database_name
        self.letsencrypt = letsencrypt
        self.wordpress_auth_vars = wordpress_auth_vars
        self.domain = domain
        self.email = email
        self.test_cert = test_cert


    def _init_inventory(self):
        self.private_data_helper.add_inventory_groups('all')
        self.private_data_helper.add_inventory_host(self.host, 'all')
        self.private_data_helper.set_inventory_ansible_user(self.host, self.user)
        self.private_data_helper.write_inventory()


    def _update_env(self):
        extravars = [
            'database_root_password',
            'database_username',
            'database_password',
            'database_name',
            'wordpress_auth_vars',
            'domain',
            'email',
            'service_to_encrypt',
            'test_cert',
        ]
        for varname in extravars:
            try:
                if varname == 'service_to_encrypt':
                    value = self.action
                    if value == 'redmine':
                        self.private_data_helper.set_extravar('port_to_encrypt', 3000)
                    else:
                        self.private_data_helper.set_extravar('port_to_encrypt', 80)
                elif varname == 'test_cert':
                    value = self.get_certbot_test_cert_string()
                elif varname == 'domain':
                    if not self.domain:
                        value = self.host
                    else:
                        value = self.domain
                else:
                    value = getattr(self, varname)

                self.private_data_helper.set_extravar(varname, value)
            except AttributeError:
                pass
        self.private_data_helper.write_env()


    def set_runner_config_var(self, var, val):
        setattr(self.runner_config, var, val)


    def set_playbook(self, playbook):
        self.set_runner_config_var('playbook', playbook)


    def _prepare_config(self):
        self.runner_config.prepare()


    def run(self):
        self._update_env()
        self._prepare_config()
        self.runner.run()

        if self.letsencrypt:
            self.set_playbook('letsencrypt.yml')
            self._update_env()
            self._prepare_config()
            self.runner.run()


    def cleanup_private_data(self):
        self.private_data_helper.cleanup_dir()


    # TODO: Looks like this isn't being used yet.
    def get_certbot_domains_string(self):
        try:
            return '-d {}'.format(' -d '.join(self.domains_for_ssl))
        except TypeError:
            return ''


    def get_certbot_test_cert_string(self):
        return '--test-cert' if self.test_cert else ''
