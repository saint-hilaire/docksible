import os
import unittest
from getpass import getpass, getuser
import yaml
from docksible.constants import TEMPLATES_DIR
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
            database_name='test_db',
        )

        if user != 'root':
            self.docksible.sudo_password = getpass(
                'Please enter sudo password for test host: '
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


    def test_nginx(self):
        self.docksible.letsencrypt = False
        self.docksible.set_action('nginx')
        self._do_test_run()


    def test_wordpress(self):
        self.docksible.database_name = 'wordpress'
        self.docksible.site_title = 'My WordPress Site'
        self.docksible.admin_username = 'admin'
        self.docksible.admin_password = 'password'
        self.docksible.admin_email = 'me@me.me'
        self.docksible.wordpress_locale = 'en_US'

        self.docksible.set_action('wordpress')
        # TODO: Get rid of this.
        self.docksible.wordpress_auth_vars = get_wordpress_auth_vars()
        self._do_test_run()


    def test_redmine(self):
        self.docksible.database_name = 'redmine'
        self.docksible.set_action('redmine')
        self._do_test_run()


    def test_ssh_proxy(self):
        self.docksible.ssh_proxy = True
        # TODO: We should have some barebones Nginx action.
        self.docksible.database_name = 'redmine'
        self.docksible.set_action('redmine')
        self._do_test_run()


    def test_custom_app(self):
        self.docksible.set_action('custom-app')
        self.docksible.database_name = 'smartestate'
        self.docksible.app_name = 'smartestate'
        self.docksible.app_image = 'belalibrahim/smartestate'
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


    def test_phpmyadmin(self):
        # TODO: We should have some barebones Nginx action.
        self.docksible.database_name = 'redmine'
        self.docksible.set_action('redmine')
        self.docksible.phpmyadmin = True
        self._do_test_run()


    def test_playbook_builder(self):
        with open(
            os.path.join(
                TEMPLATES_DIR,
                'base-playbook.yml',
            ), 'r'
        ) as fh:
            expected_playbook_ls = yaml.safe_load(fh)

        self.docksible.set_action('setup-docker-compose')
        self.docksible._build_ansible_files()
        with open(
            os.path.join(
                self.docksible.private_data_dir,
                self.docksible.playbook_builder.playbook_filename
            ), 'r'
        ) as fh:
            written_yaml = yaml.safe_load(fh)

        self.docksible.cleanup_private_data()
        self.assertListEqual(expected_playbook_ls, written_yaml)


    def test_docker_compose_builder(self):
        with open(
            os.path.join(
                TEMPLATES_DIR,
                'base-docker-compose.yml.j2',
            ), 'r'
        ) as fh:
            expected_docker_compose = yaml.safe_load(fh)

        self.docksible.set_action('nginx')
        self.docksible._build_ansible_files()
        with open(
            os.path.join(
                self.docksible.private_data_dir,
                'templates',
                'docker-compose.yml.j2',
            ), 'r'
        ) as fh:
            written_yaml = yaml.safe_load(fh)

        self.docksible.cleanup_private_data()
        self.assertDictEqual(expected_docker_compose, written_yaml)


    def test_nginx_conf_builder(self):

        self.docksible.set_action('nginx')
        self.docksible._build_ansible_files()

        expected = os.path.join('test', 'expected-nginx.conf')
        actual = os.path.join(self.docksible.private_data_dir, 'templates', 'nginx.conf.j2')

        with open(expected, 'r', encoding='utf-8') as f1, open(actual, 'r', encoding='utf-8') as f2:
            self.docksible.cleanup_private_data()
            assert f1.read().strip().replace('\r\n', '\n') == f2.read().strip().replace('\r\n', '\n')


    def test_v1(self):
        print('TESTING DEV VERSION 1')
        print("GOAL: Refactor the application so that all of 'src/docksible/project/' \
              gets generated dynamically by DocksiblePlaybookBuilder")
        print('To make it easier, do this:')
        print('* git checkout dev/v1')
        print('* cp -r src/docksible/project/* test/tmp-private-data/')
        print('* git checkout refactor/gh-24-docker-compose')
        print('Continue debugging the following code ;-)')
        import pdb; pdb.set_trace()
        self.docksible.letsencrypt = False
        self._do_test_run()


    def _do_test_run(self):
        self.assertEqual(self.docksible.run(), 0)
