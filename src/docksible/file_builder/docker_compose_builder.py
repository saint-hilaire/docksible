import os
import yaml

from docksible.constants import TEMPLATES_DIR
from .docksible_file_builder import DocksibleFileBuilder


class DockerComposeBuilder(DocksibleFileBuilder):

    def __init__(self, private_data_dir, action,
            database_root_password=None, database_username=None,
            database_password=None, database_name=None,
    ):
        super().__init__(
                private_data_dir,
                'base-docker-compose.yml.j2',
                action,
        )
        self.docker_compose_services = self.base_template['services']

        self.database_root_password = database_root_password
        self.database_username = database_username
        self.database_password = database_password
        self.database_name = database_name


    def add_db_service(self):
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


    def add_app_service(self):
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
                '{{ ansible_env.HOME }}/docker-compose-volumes/wordpress-data:/var/www/html'
            ]
            import pdb; pdb.set_trace()
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


    def add_webserver_config(self):
        # TODO: Similar to the other methods above, the 'docksible_webserver'
        # service will need to be adjusted slightly based on whatever action
        # we have.
        # I also want to rename this method then.
        pass



    def set_action(self, action):
        self.action = action
        if action not in ['setup-docker-compose', 'nginx']:
            self.add_db_service()
            self.add_app_service()
            self.add_webserver_config()


    def write(self, filepath=['templates', 'docker-compose.yml.j2']):
        super().write(filepath)
