from .docksible_file_builder import DocksibleFileBuilder


class PlaybookBuilder(DocksibleFileBuilder):

    def __init__(self, private_data_dir, action):

        super().__init__(
                private_data_dir,
                'base-playbook.yml',
                action
        )

        self._playbook_dict = self.base_template[0]


    def set_action(self, action):
        self.action = action
        self.playbook_filename = f'{action}.yml'

        if action != 'setup-docker-compose':
            self._playbook_dict['tasks'].extend([
                {
                    'name': 'Copy the Nginx Configuration',
                    'template': {
                        'src': 'nginx.conf.j2',
                        'dest': '{{ ansible_env.HOME }}/docker-compose-volumes/nginx-data/nginx.conf',
                        # TODO: Here, and elsewhere, perhaps we can just pass in
                        # Docksible's 'user' parameter?
                        'owner': '{{ ansible_user }}',
                        'group': '{{ ansible_user }}',
                        'mode': '0644',
                    },
                },
                {
                    'name': 'Load Docker-Compose file',
                    'template': {
                        'src': 'docker-compose.yml.j2',
                        'dest': '{{ ansible_env.HOME }}/docker-compose/docker-compose.yml',
                        # TODO: Here, and elsewhere, perhaps we can just pass in
                        # Docksible's 'user' parameter?
                        'owner': '{{ ansible_user }}',
                        'group': '{{ ansible_user }}',
                        'mode': '0600'
                    },
                },
                {
                    # TODO: Maybe these snippets also belong in template files?
                    'name': 'Run the web service',
                    'community.docker.docker_compose_v2': {
                        'project_src': '{{ ansible_env.HOME }}/docker-compose/'
                    },
                },
            ])


    def write(self, filepath=[]):
        filepath = [self.playbook_filename]
        super().write(filepath)
