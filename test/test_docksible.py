import os
import unittest
from getpass import getpass, getuser
from docksible.docksible import Docksible
# TODO: Get rid of this.
from docksible.helpers import get_wordpress_auth_vars


class TestDocksible(unittest.TestCase):

    def setUp(self):
        try:
            tmp_remote = os.environ['DOCKSIBLE_REMOTE'].split('@')
            user = tmp_remote[0]
            host = tmp_remote[1]
        except IndexError:
            user = getuser()
            host = 'localhost'
        except KeyError:
            exit("Please set environment variable 'DOCKSIBLE_REMOTE'!")

        self.docksible = Docksible(
            user=user,
            host=host,
            action='setup-docker-compose',
            private_data_dir=os.path.join(
                'test',
                'tmp-private-data',
            ),
            database_root_password='rootpassword',
            database_username='db-username',
            database_password='password',
        )

        if host in ['localhost', '127.0.0.1']:
            self.docksible.sudo_password = getpass(
                'Please enter local sudo password: '
            )
            self.docksible.letsencrypt = False
        else:
            self.docksible.letsencrypt = True
            self.docksible.domain = host
            self.docksible.email = 'user@example.com'
            self.docksible.test_cert = True


    def test_wordpress(self):
        self.docksible.database_name = 'wordpress'
        self.docksible.action = 'wordpress'
        # TODO: Improve this.
        self.docksible.set_playbook('wordpress.yml')
        # TODO: Get rid of this.
        self.docksible.wordpress_auth_vars = get_wordpress_auth_vars()
        self._do_test_run()


    def test_redmine(self):
        self.docksible.database_name = 'redmine'
        self.docksible.action = 'redmine'
        # TODO: Improve this.
        self.docksible.set_playbook('redmine.yml')
        self._do_test_run()


    def _do_test_run(self):
        self.docksible.run()
        # TODO
        assert 0 == 0


    def tearDown(self):
        self.docksible.cleanup_private_data()
