import os
import yaml

from docksible.constants import PROJECT_DIR


class DocksiblePlaybookBuilder:

    def __init__(self, private_data_dir, action):
        self.private_data_dir = private_data_dir
        self.playbook_filename = f'{action}.yml'

        with open(
            os.path.join(
                PROJECT_DIR,
                'base-setup-docker-compose.yml'
            ), 'r'
        ) as fh:
            self.playbook = yaml.safe_load(fh)

        self._playbook_dict = self.playbook[0]

        self.set_action(action)


    def add_role(self, role):
        pass
        # TODO: Not doing it with Roles anymore
        #self._playbook_dict['roles'].append(role)


    def set_action(self, action):
        self.action = action
        # TODO: Not doing it with Roles anymore
        #if action != 'setup-docker-compose':
        #    self.add_role(action)


    def write(self):
        with open(
            os.path.join(self.private_data_dir, self.playbook_filename), 'w'
        ) as fh:
            yaml.dump(self.playbook, fh)
