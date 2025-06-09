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
            # 'user@example.com' will be rejected by Let's Encrypt,
            # but 'me@me.me' seems OK...
            # And Docksible fails silently... we could maybe
            # improve that as well...
            #self.docksible.email = 'user@example.com'
            self.docksible.email = 'me@me.me'
            self.docksible.test_cert = True


    def test_docker_compose(self):
        self.docksible.letsencrypt = False
        self._do_test_run()


    def test_wordpress(self):
        self.docksible.database_name = 'wordpress'
        self.docksible.action = 'wordpress'
        # TODO: Get rid of this.
        self.docksible.wordpress_auth_vars = get_wordpress_auth_vars()
        self._do_test_run()


    def test_redmine(self):
        self.docksible.database_name = 'redmine'
        self.docksible.action = 'redmine'
        self._do_test_run()


    def test_ssh_proxy(self):
        self.docksible.ssh_proxy = True
        # TODO: We should have some barebones Nginx action.
        self.docksible.database_name = 'redmine'
        self.docksible.action = 'redmine'
        self._do_test_run()


    def test_custom_app(self):
        self.docksible.action = 'custom-app'
        self.docksible.database_name = 'smartestate'
        self.docksible.app_name = 'smartestate'
        self.docksible.app_image = 'sainthilaire/smartestate:latest'
        self.docksible.extra_env_vars = {
            'DEBUG': 0,
            'ALLOWED_HOSTS': self.docksible.host,
            'DATABASE_ENGINE': 'django.db.backends.mysql',
            'DATABASE_HOST': 'docksible_db',
            'DATABASE_NAME': self.docksible.database_name,
            'DATABASE_USER': self.docksible.database_username,
            'DATABASE_PASSWORD': self.docksible.database_password,
        }
        self._do_test_run()


    def _do_test_run(self):
        self.assertEqual(self.docksible.run(), 0)
