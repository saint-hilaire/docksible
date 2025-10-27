import os
from .docksible_file_builder import DocksibleFileBuilder


class DockerComposeBuilder(DocksibleFileBuilder):

    def __init__(self, private_data_dir, action):
        super().__init__(
                private_data_dir,
                'docker-compose.yml.j2',
                action,
        )
        self.set_action(action)


    def set_action(self, action):
        self.action = action
        # TODO...


    def write(self, filepath=['templates', 'docker-compose.yml.j2']):
        try:
            os.makedirs(
                os.path.join(self.private_data_dir, 'templates'),
                exist_ok=True
            )
        except FileExistsError:
            pass

        super().write(filepath)
