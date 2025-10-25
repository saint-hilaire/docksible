import os
from sys import path as sys_path
from secrets import token_hex


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
