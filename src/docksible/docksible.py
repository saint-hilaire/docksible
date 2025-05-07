from shutil import rmtree
from ansible_runner import interface as runner_interface
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
            ssh_proxy=False,
            sudo_password=None,
            apparmor_workaround=False,
        ):
        self.private_data_dir = private_data_dir
        try:
            os.makedirs(self.private_data_dir)
        except FileExistsError:
            pass

        self.user   = user
        self.host   = host

        host_dict = {'ansible_user': self.user}
        if self.host in ['localhost', '127.0.0.1']:
            host_dict['ansible_connection'] = 'local'

        self.inventory = {
            'all': {
                'hosts': {
                    self.host: host_dict,
                },
            },
            'ungrouped': {'hosts': {}},
        }

        self.action = action

        self.database_root_password = database_root_password
        self.database_username = database_username
        self.database_password = database_password
        self.database_name = database_name
        self.letsencrypt = letsencrypt
        self.wordpress_auth_vars = wordpress_auth_vars
        self.domain = domain
        self.email = email
        self.test_cert = test_cert
        self.ssh_proxy = ssh_proxy
        self.sudo_password = sudo_password

        self.extravars = {}

        self.apparmor_workaround = apparmor_workaround


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
            'ssh_proxy',
            'ansible_sudo_pass',
            'apparmor_workaround',
        ]
        for varname in extravars:
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


    def run(self):
        self._update_env()
        runner = runner_interface.run(
            private_data_dir=self.private_data_dir,
            playbook=f'{self.action}.yml',
            inventory=self.inventory,
            extravars=self.extravars,
            project_dir=PROJECT_DIR,
        )
        if runner.rc != 0:
            self.cleanup_private_data()
            return runner.rc

        if self.letsencrypt:
            runner = runner_interface.run(
                private_data_dir=self.private_data_dir,
                playbook='letsencrypt.yml',
                inventory=self.inventory,
                extravars=self.extravars,
                project_dir=PROJECT_DIR,
            )
            if runner.rc != 0:
                self.cleanup_private_data()
                return runner.rc

        self.cleanup_private_data()
        return runner.rc


    def cleanup_private_data(self):
        rmtree(self.private_data_dir)


    # TODO: Looks like this isn't being used yet.
    def get_certbot_domains_string(self):
        try:
            return '-d {}'.format(' -d '.join(self.domains_for_ssl))
        except TypeError:
            return ''


    def get_certbot_test_cert_string(self):
        return '--test-cert' if self.test_cert else ''
