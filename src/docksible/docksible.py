from shutil import rmtree
import subprocess
from ansible_runner import interface as runner_interface
from .constants import *
from .helpers import *
from .file_builder.playbook_builder import PlaybookBuilder
from .file_builder.docker_compose_builder import DockerComposeBuilder
from .file_builder.nginx_conf_builder import NginxConfBuilder


class Docksible:

    def __init__(self, user, host, action,
            private_data_dir=DEFAULT_PRIVATE_DATA_DIR,
            database_root_password=None, database_username=None,
            database_password=None, database_name=None,
            letsencrypt=False,
            domain=None, email=None,
            test_cert=False,
            ssh_proxy=False,
            sudo_password=None,
            app_image=None,
            app_name=None,
            app_version=DEFAULT_APP_VERSION,
            site_title=DEFAULT_SITE_TITLE,
            admin_username=DEFAULT_ADMIN_USERNAME,
            admin_password=None,
            admin_email=DEFAULT_ADMIN_EMAIL,
            wordpress_locale=DEFAULT_WORDPRESS_LOCALE,
            manual_app_install=False,
            internal_http_port=DEFAULT_INTERNAL_HTTP_PORT,
            phpmyadmin=False,
            extra_env_vars={},
            apparmor_workaround=False,
        ):

        self.private_data_dir = private_data_dir
        try:
            os.makedirs(
                os.path.join(
                    self.private_data_dir,
                    'templates',
                )
            )
        except FileExistsError:
            pass

        self.user = user
        self.host = host

        host_dict = {'ansible_user': self.user}

        if host_is_local(self.host):
            host_dict['ansible_connection'] = 'local'

        self.inventory = {
            'all': {
                'hosts': {
                    self.host: host_dict,
                },
            },
            'ungrouped': {'hosts': {}},
        }

        self.app_image = app_image
        self.app_version = app_version

        self.database_root_password = database_root_password
        self.database_username = database_username
        self.database_password = database_password
        self.database_name = database_name

        self.letsencrypt = letsencrypt
        self.domain = domain
        self.email = email
        self.test_cert = test_cert

        self.site_title = site_title
        self.admin_username = admin_username
        self.admin_password = admin_password
        self.admin_email = admin_email
        self.wordpress_locale = wordpress_locale

        self.app_name = app_name
        self.internal_http_port = internal_http_port
        self.phpmyadmin = phpmyadmin
        self.manual_app_install = manual_app_install
        self.extra_env_vars = extra_env_vars

        self.ssh_proxy = ssh_proxy
        self.sudo_password = sudo_password
        self.apparmor_workaround = apparmor_workaround
        self.extravars = {}

        self.set_action(action)


    def set_action(self, action):
        self.action = action

        if action != 'custom-app':
            self.app_image = action

        self.playbook_builder = PlaybookBuilder(
            self.private_data_dir,
            self.action,
            self.letsencrypt,
        )
        self.docker_compose_builder = DockerComposeBuilder(
            self.private_data_dir,
            self.action,
            self.letsencrypt,
            database_root_password=self.database_root_password,
            database_username=self.database_username,
            database_password=self.database_password,
            database_name=self.database_name,
            manual_app_install=self.manual_app_install,
        )
        self.nginx_conf_builder = NginxConfBuilder(
            self.private_data_dir,
            self.action,
            self.letsencrypt,
        )

        # TODO: Move these to the above constructors?
        # TODO: Continue here for letsencrypt. So far, the flag has been
        # passed along correctly.
        self.playbook_builder.set_action(self.action)
        self.docker_compose_builder.set_action(self.action)
        self.nginx_conf_builder.set_action(self.action)


    # TODO: Rename this to something more appropriate.
    # It sets the extravars...
    def _update_env(self):
        if self.action == 'redmine':
            self.internal_http_port = 3000
        elif self.action == 'wordpress':
            self.internal_http_port = 80

        extravars = [
            'docker_compose_volume_dirs',
            'app_version',
            'database_root_password',
            'database_username',
            'database_password',
            'database_name',
            'domain',
            'email',
            'service_to_encrypt',
            'test_cert',
            'ssh_proxy',
            'ansible_sudo_pass',
            'app_image',
            'app_name',
            'site_title',
            'admin_username',
            'admin_password',
            'admin_email',
            'wordpress_locale',
            'internal_http_port',
            'phpmyadmin',
            'extra_env_vars',
            'apparmor_workaround',
        ]
        for varname in extravars:
            if varname == 'docker_compose_volume_dirs':
                value = [
                    'db-data',
                    'nginx-data',
                    'app-data',
                ]
                if self.ssh_proxy:
                    value.append('ssh-proxy-data')
                if self.letsencrypt:
                    value.append('certbot-data')

            elif varname == 'service_to_encrypt':
                # TODO: Tech debt. Fix in v1. I want to prefer dashes over
                # underscores, but for now, I need it like this.
                value = self.action.replace('-', '_')

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


    def _build_ansible_files(self):
        self.playbook_builder.write()
        self.docker_compose_builder.write()
        self.nginx_conf_builder.write()


    def _install_galaxy_dependencies(self):
        subprocess.run([
            'ansible-galaxy',
            'collection',
            'install',
            'community.docker',
        ])


    def run(self):
        self._update_env()
        self._build_ansible_files()
        self._install_galaxy_dependencies()

        runner = runner_interface.run(
            private_data_dir=self.private_data_dir,
            playbook=f'{self.action}.yml',
            inventory=self.inventory,
            extravars=self.extravars,
        )

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
