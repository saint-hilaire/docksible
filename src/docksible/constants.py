import os
from .helpers import *

USER_HOME_DIR = os.path.expanduser('~')
TEMPLATES_DIR = find_templates_dir()
DEFAULT_PRIVATE_DATA_DIR = os.path.join(USER_HOME_DIR, '.docksible')
DEFAULT_BACKUPS_DIR = os.path.join(USER_HOME_DIR, '.docksible-backups')

SUPPORTED_ACTIONS = [
    'setup-docker-compose',
    'nginx',
    'redmine',
    'wordpress',
    'backup',
    'custom-app',
]

DEFAULT_DATABASE_USERNAME = 'db-username'
DEFAULT_DATABASE_NAME = 'db_name'
DEFAULT_DATABASE_TABLE_PREFIX = ''

DEFAULT_SITE_TITLE     = 'Sample Site'
DEFAULT_ADMIN_USERNAME = 'admin'
DEFAULT_ADMIN_EMAIL    = 'admin@example.com'

DEFAULT_WORDPRESS_LOCALE = 'en_US'

DEFAULT_APP_VERSION = 'latest'

DEFAULT_INTERNAL_HTTP_PORT = 8000
