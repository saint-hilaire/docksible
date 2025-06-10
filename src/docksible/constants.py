import os
from .helpers import *

USER_HOME_DIR = os.path.expanduser('~')
PROJECT_DIR = find_package_project_dir()
DEFAULT_PRIVATE_DATA_DIR = os.path.join(USER_HOME_DIR, '.docksible')
DEFAULT_BACKUPS_DIR = os.path.join(USER_HOME_DIR, '.docksible-backups')

SUPPORTED_ACTIONS = [
    'setup-docker-compose',
    'redmine',
    'wordpress',
    'backup',
    'custom-app',
]

DEFAULT_DATABASE_USERNAME = 'db-username'
DEFAULT_DATABASE_NAME = 'db_name'
DEFAULT_DATABASE_TABLE_PREFIX = ''

DEFAULT_INTERNAL_HTTP_PORT = 8000
