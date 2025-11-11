import os
import crossplane
from docksible.constants import TEMPLATES_DIR
from .docksible_file_builder import DocksibleFileBuilder


class NginxConfBuilder(DocksibleFileBuilder):

    def __init__(self, private_data_dir, action):
        self.private_data_dir = private_data_dir

        self.base_template = crossplane.parse(
                os.path.join(TEMPLATES_DIR, 'base-nginx.conf.j2'))

        # TODO: Is there a better way?
        self.nginx_conf = self.base_template['config'][0]['parsed'][0]['block']
        self._server_block = self.nginx_conf[0]['block']


    def set_action(self, action):
        self.action = action

        if action == 'nginx':
            return

        if action in ['redmine']:
            self.app_port = 3000
        else:
            self.app_port = 80

        root_location_block = [
            {
                'directive': 'proxy_pass',
                'args': ['http://docksible_app:{}'.format(self.app_port)],
            },
            {
                'directive': 'proxy_set_header',
                'args': ['Host', '$host'],
            },
            {
                'directive': 'proxy_set_header',
                'args': ['X-Real-IP', '$remote_addr'],
            },
        ]

        found_it = False
        for conf_dict in self._server_block:
            if conf_dict['directive'] == 'location' \
                    and conf_dict['args'] == ['/']:
                conf_dict['block'] = root_location_block
                found_it = True
        if not found_it:
            raise RuntimeError('Found no root location block in nginx_conf')

        if action == 'wordpress':
            self._server_block.append({
                'directive': 'location',
                'args': ['/xmlrpc.php'],
                'block': [
                    {'directive': 'deny', 'args': ['all']},
                    {'directive': 'access_log', 'args': ['off']},
                ],
            })


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
