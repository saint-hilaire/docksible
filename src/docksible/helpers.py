import os
from sys import path as sys_path
from secrets import token_hex


def find_package_project_dir():
    for path_str in sys_path:
        try:
            try_path = os.path.join(path_str, 'docksible', 'project')
            assert os.path.isdir(try_path)
            return try_path
        except AssertionError:
            pass
    raise RuntimeError("Got no user supplied --project-dir, and could not find one in expected package location. Your Docksible installation is likely broken. However, if you are running this code directly from source, this is expected behavior. You probably forgot to pass the '--project-dir' flag. The directoy you're looking for is 'src/docksible/project/'.")


# TODO: In the future we shouldn't use this, because we let WP-CLI handle these instead.
def get_wordpress_auth_vars():
    auth_var_names = [
        'auth_key',
        'secure_auth_key',
        'logged_in_key',
        'nonce_key',
        'auth_salt',
        'secure_auth_salt',
        'logged_in_salt',
        'nonce_salt',
    ]
    auth_vars = {}

    for var in auth_var_names:
        auth_vars['WORDPRESS_{}'.format(var.upper())] = token_hex(64)

    return auth_vars
