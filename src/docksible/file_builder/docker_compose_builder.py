import os
import yaml

from docksible.constants import TEMPLATES_DIR
from .docksible_file_builder import DocksibleFileBuilder


class DockerComposeBuilder(DocksibleFileBuilder):

    def __init__(self, private_data_dir, action, letsencrypt=False,
            database_root_password=None, database_username=None,
            database_password=None, database_name=None,
            manual_app_install=False, phpmyadmin=False
    ):
        super().__init__(
            private_data_dir,
            'base-docker-compose.yml.j2',
            action,
            letsencrypt,
        )
        self.docker_compose_services = self.base_template['services']

        self.database_root_password = database_root_password
        self.database_username = database_username
        self.database_password = database_password
        self.database_name = database_name

        self.manual_app_install = manual_app_install

        self.set_action(action)
        self.set_letsencrypt(letsencrypt)


    def _add_db_service(self):
        with open(
            os.path.join(
                TEMPLATES_DIR,
                'db-docker-compose.yml.j2'
            )
        ) as fh:
            self.docker_compose_services['docksible_db'] = \
                    yaml.safe_load(fh)['docksible_db']

        if self.action == 'wordpress':
            # TODO: Necessary? I saw this in the legacy version.
            self.docker_compose_services['docksible_db']['command'] = \
                    '--default-authentication-plugin=mysql_native_password'

        #if self.phpmyadmin:
        #    self.docker_compose_services['docksible_phpmyadmin'] = \
        #            self.get_additional_template('phpmyadmin-service.yml.j2')[
        #                    'docksible_phpmyadmin']


    def _add_app_service(self):
        with open(
            os.path.join(
                TEMPLATES_DIR,
                'app-docker-compose.yml.j2'
            )
        ) as fh:
            self.docker_compose_services['docksible_app'] = \
                    yaml.safe_load(fh)['docksible_app']

        if self.action == 'wordpress':
            self.docker_compose_services['docksible_app']['environment'] = {
                'WORDPRESS_DB_HOST': 'docksible_db',
                'WORDPRESS_DB_USER': self.database_username,
                'WORDPRESS_DB_PASSWORD': self.database_password,
                'WORDPRESS_DB_NAME': self.database_name,
            }
            self.docker_compose_services['docksible_app']['volumes'] = [
                '{{ ansible_env.HOME }}/docker-compose-volumes/app-data:/var/www/html'
            ]
            if not self.manual_app_install:
                self._add_auxiliary_service('wp-cli-service.yml.j2')

        elif self.action == 'redmine':
            self.docker_compose_services['docksible_app']['environment'] = {
                'REDMINE_DB_MYSQL': 'docksible_db',
                'REDMINE_DB_PASSWORD': self.database_root_password,
            }
            self.docker_compose_services['docksible_app']['security_opt'] = [
                # TODO: Necessary? I saw this in the legacy version.
                'seccomp:unconfined'
            ]


    def _add_auxiliary_service(self, service_template_name):
        self.docker_compose_services['docksible_auxiliary'] = \
                self.get_additional_template(
                        service_template_name)['docksible_auxiliary']


    def _add_letsencrypt_config(self):
        if self.letsencrypt:
            self.docker_compose_services['docksible_webserver']['volumes'].append(
                '{{ ansible_env.HOME }}/docker-compose-volumes/certbot-data:/etc/letsencrypt'
            )
            self.docker_compose_services['docksible_certbot'] = \
                    self.get_additional_template(
                            'letsencrypt-docker-compose.yml.j2')['docksible_certbot']


    def write(self, filepath=['templates', 'docker-compose.yml.j2']):
        if self.action not in ['setup-docker-compose', 'nginx']:
            self._add_db_service()
            self._add_app_service()
            self._add_letsencrypt_config()

        super().write(filepath)
