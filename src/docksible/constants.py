import os
from .helpers import *

USER_HOME_DIR = os.path.expanduser('~')
PROJECT_DIR = find_package_project_dir()
DEFAULT_PRIVATE_DATA_DIR = os.path.join(USER_HOME_DIR, '.docksible')
DEFAULT_BACKUPS_DIR = os.path.join(USER_HOME_DIR, '.docksible-backups')
DEFAULT_DATABASE_USERNAME = 'db-username'
DEFAULT_DATABASE_NAME = 'db_name'
DEFAULT_DATABASE_TABLE_PREFIX = ''
