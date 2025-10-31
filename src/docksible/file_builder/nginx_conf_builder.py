import os
import crossplane
from docksible.constants import TEMPLATES_DIR
from .docksible_file_builder import DocksibleFileBuilder


class NginxConfBuilder(DocksibleFileBuilder):

    def __init__(self, private_data_dir, action):
        self.private_data_dir = private_data_dir

        self.base_template = crossplane.parse(
                os.path.join(TEMPLATES_DIR, 'base-nginx.conf'))

        # TODO: Is there a better way?
        self.nginx_conf = self.base_template['config'][0]['parsed']


    def set_action(self, action):
        self.action = action
        # TODO...


    def write(self, filepath=['templates', 'nginx.conf.j2']):
        with open(
            os.path.join(
                self.private_data_dir,
                *filepath
            ), 'w'
        ) as fh:
            fh.write(
                crossplane.build(
                    self.nginx_conf
                )
            )
