import os
import yaml


class DocksiblePlaybookBuilder:

    def __init__(self, private_data_dir, action):
        self.private_data_dir = private_data_dir
        self.action = action
        self.playbook_filename = f'{action}.yml'
        self._playbook_dict = {
            'hosts': 'all',
            'become': True,
            'gather_facts': True,
            'roles': [
                'setup-docker-compose',
            ],
        }
        self.playbook = [self._playbook_dict]

        self.set_action(action)


    def add_role(self, role):
        self._playbook_dict['roles'].append(role)


    def set_action(self, action):
        if action != 'setup-docker-compose':
            self.add_role(action)


    def write(self):
        with open(
            os.path.join(self.private_data_dir, self.playbook_filename), 'w'
        ) as fh:
            yaml.dump(self.playbook, fh)
