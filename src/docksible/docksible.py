from ansible_runner import (
    Runner,
    RunnerConfig,
    interface as runner_interface
)
from .constants import *


class Docksible:

    def __init__(self, user, host, action,
            private_data_dir=DEFAULT_PRIVATE_DATA_DIR,
            database_root_password=None, database_username=None,
            database_password=None, database_name=None,
            letsencrypt=False,
            wordpress_auth_vars=None,
            domain=None, email=None,
            test_cert=False,
            sudo_password=None
        ):
        self.private_data_dir = private_data_dir

        self.user   = user
        self.host   = host
        self.action = action

        self._init_inventory()

        # TODO: Get rid of runner_config.
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
        self.sudo_password = sudo_password


    def _init_inventory(self):
        self.inventory = {
            'all': {
                'hosts': {
                    self.host: {
                        'ansible_user': self.user,
                        'inventory_dir': None,
                        'inventory_file': None,
                    },
                },
            },
            'ungrouped': {'hosts': {}},
        }


    def _update_env(self):
        self.extravars = {}
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
            'ansible_sudo_pass',
        ]
        for varname in extravars:
            try:
                if varname == 'service_to_encrypt':
                    value = self.action
                    if value == 'redmine':
                        self.extravars['port_to_encrypt'] = 3000
                    else:
                        self.extravars['port_to_encrypt'] = 80
                elif varname == 'test_cert':
                    value = self.get_certbot_test_cert_string()
                elif varname == 'domain':
                    if not self.domain:
                        value = self.host
                    else:
                        value = self.domain
                elif varname == 'ansible_sudo_pass':
                    if self.sudo_password:
                        value = self.sudo_password
                    else:
                        continue
                else:
                    value = getattr(self, varname)

                self.extravars[varname] = value
            except AttributeError:
                pass


    # TODO: Get rid of runner_config.
    def set_runner_config_var(self, var, val):
        setattr(self.runner_config, var, val)


    def set_playbook(self, playbook):
        self.set_runner_config_var('playbook', playbook)


    # TODO: Get rid of runner_config.
    def _prepare_config(self):
        self.runner_config.prepare()


    def run(self):
        self._update_env()
        # TODO: Get rid of runner_config.
        self._prepare_config()
        runner = runner_interface.run(
            private_data_dir=self.private_data_dir,
            playbook=f'{self.action}.yml',
            inventory=self.inventory,
            extravars=self.extravars,
            project_dir=PROJECT_DIR,
        )
        # TODO: return code handling.
        rc = 0 if runner else 1

        if self.letsencrypt:
            runner = runner_interface.run(
                private_data_dir=self.private_data_dir,
                playbook='letsencrypt.yml',
                inventory=self.inventory,
                extravars=self.extravars,
                project_dir=PROJECT_DIR,
            )
            #self.set_playbook('letsencrypt.yml')
            #self._update_env()
            #self._prepare_config()
            #self.runner.run()


    # TODO: Make sure it gets deleted - safely.
    def cleanup_private_data(self):
        pass


    # TODO: Looks like this isn't being used yet.
    def get_certbot_domains_string(self):
        try:
            return '-d {}'.format(' -d '.join(self.domains_for_ssl))
        except TypeError:
            return ''


    def get_certbot_test_cert_string(self):
        return '--test-cert' if self.test_cert else ''
