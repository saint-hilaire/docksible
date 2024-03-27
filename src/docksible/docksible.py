import os
import argparse
import textwrap
from ansible_runner import Runner, RunnerConfig

# Shouldn't need these.
# import shlex
# from subprocess import run, Popen, PIPE
# from time import sleep

# Will probably need this later.
# from secrets import token_hex


__author__ = "Brian St. Hilailre"
__copyright__ = "Copyright 2022, Sanctus Technologies UG (haftungsb.)"
__license__ = "Apache License, Version 2.0"
__version__ = "0.2"
__maintainer__ = "Brian St. Hilaire"
__email__ = "brian.st-hilaire@sanctus-tech.com"

USER_HOME_DIR = os.path.expanduser('~')
DEFAULT_PRIVATE_DATA_DIR = os.path.join(USER_HOME_DIR, '.docksible')


# TODO
def init_private_data_dir():
    try:
        os.makedirs(DEFAULT_PRIVATE_DATA_DIR)
    except FileExistsError:
        pass
    return DEFAULT_PRIVATE_DATA_DIR


# TODO: Refactor this into the library - see Lampsible.
def prepare_inventory(user, host):
    return '{}@{},'.format(user, host)


# TODO: Refactor this into the library - see Lampsible.
# Obviously, improve this!
def cleanup_private_data_dir(path):
    os.system('rm -r ' + path)


# @deprecated
def do_bootstrap(user, host):
    pass


def do_services(
    user,
    host,
    db_root_passwd,
    db_user,
    db_passwd,
    db_name,
    wp_auth_key,
    wp_secure_auth_key,
    wp_logged_in_key,
    wp_nonce_key,
    wp_auth_salt,
    wp_secure_auth_salt,
    wp_logged_in_salt,
    wp_nonce_salt
):
    pass
    # replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", 
    #     host + "    ansible_python_interpreter=/usr/bin/python3")
    # os.chdir(dawn_path+"/ansible")

    # ansible_cmd = 'ansible-playbook -u {user} -i hosts playbook.yml \
    #     --extra-vars "db_root_passwd={db_root_passwd} \
    #     db_user={db_user} \
    #     db_passwd={db_passwd} \
    #     db_name={db_name} \
    #     wp_auth_key={wp_auth_key} \
    #     wp_secure_auth_key={wp_secure_auth_key} \
    #     wp_logged_in_key={wp_logged_in_key} \
    #     wp_nonce_key={wp_nonce_key} \
    #     wp_auth_salt={wp_auth_salt} \
    #     wp_secure_auth_salt={wp_secure_auth_salt} \
    #     wp_logged_in_salt={wp_logged_in_salt} \
    #     wp_nonce_salt={wp_nonce_salt}"'.format(
    #         user=user,
    #         db_root_passwd=db_root_passwd,
    #         db_user=db_user,
    #         db_passwd=db_passwd,
    #         db_name=db_name,
    #         wp_auth_key=wp_auth_key,
    #         wp_secure_auth_key=wp_secure_auth_key,
    #         wp_logged_in_key=wp_logged_in_key,
    #         wp_nonce_key=wp_nonce_key,
    #         wp_auth_salt=wp_auth_salt,
    #         wp_secure_auth_salt=wp_secure_auth_salt,
    #         wp_logged_in_salt=wp_logged_in_salt,
    #         wp_nonce_salt=wp_nonce_salt
    #     )
    # os.system(ansible_cmd)
    # os.system("git restore hosts")
    

def do_custom_service(
    user,
    host,
    domain,
    database_root_password,
    database_user,
    database_password,
    database_name,
    service_name,
    app_name,
    # TODO: The playbook also needs to SSH-keyscan the webservice
    # (i.e. GitHub), where the repo is hosted, so that the playbook can clone
    # the repository. Possibly also need to load a user's SSH key, if the repo
    # is private. Otherwise, the user needs to do this manually.
    django_app_repository,
    django_app_git_branch,
    django_dockerfile_path,
    django_secret_key,
    django_secret_key_var_name,
    host_domain_env_var_name,
    django_staticfiles_directory,
    django_media_directory,
    django_max_upload_size,
    django_upload_buffer_size,
):
    pass
    # if app_name != "":
    #     app_name_extravar = "app_name="+app_name
    # else:
    #     app_name_extravar = ""
    # if domain == "" or domain is None:
    #     domain = host
    # replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123",
    #     host + "    ansible_python_interpreter=/usr/bin/python3")
    # os.chdir(dawn_path+"/ansible")
    # ansible_cmd = 'ansible-playbook -u {user} -i hosts --extra-vars \
    #     "database_root_password={database_root_password} \
    #     database_user={database_user} database_password={database_password} \
    #     database_name={database_name} \
    #     service_name={service_name} {app_name_extravar} \
    #     domain={domain} \
    #     django_app_repository={django_app_repository} \
    #     django_app_git_branch={django_app_git_branch} \
    #     django_dockerfile_path={django_dockerfile_path} \
    #     django_secret_key={django_secret_key} \
    #     django_secret_key_var_name={django_secret_key_var_name} \
    #     host_domain_env_var_name={host_domain_env_var_name} \
    #     django_staticfiles_directory={django_staticfiles_directory} \
    #     django_media_directory={django_media_directory} \
    #     django_max_upload_size={django_max_upload_size} \
    #     django_upload_buffer_size={django_upload_buffer_size}" \
    #     {service_name}.yml'.format( # TODO: Figure out how to do this
    #                                 # conditionally in Ansible.
    #         user=user,
    #         domain=domain,
    #         database_root_password=database_root_password,
    #         database_user=database_user,
    #         database_password=database_password,
    #         database_name=database_name,
    #         service_name=service_name,
    #         app_name_extravar=app_name_extravar,
    #         django_app_repository=django_app_repository,
    #         django_app_git_branch=django_app_git_branch,
    #         django_dockerfile_path=django_dockerfile_path,
    #         django_secret_key=django_secret_key,
    #         django_secret_key_var_name=django_secret_key_var_name,
    #         host_domain_env_var_name=host_domain_env_var_name,
    #         django_staticfiles_directory=django_staticfiles_directory,
    #         django_media_directory=django_media_directory,
    #         django_max_upload_size=django_max_upload_size,
    #         django_upload_buffer_size=django_upload_buffer_size,
    # )
    # os.system(ansible_cmd)
    # os.system("git restore hosts")


def do_ssl_selfsigned(user, host, service_to_encrypt, port_to_encrypt):
    pass
    # replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123",
    #     host + "    ansible_python_interpreter=/usr/bin/python3")
    # os.chdir(dawn_path+"/ansible")
    # ansible_cmd = 'ansible-playbook -u {user} -i hosts --extra-vars \
    #     "service_to_encrypt={service_to_encrypt} \
    #     port_to_encrypt={port_to_encrypt}" ssl-selfsigned.yml'.format(
    #         user=user,
    #         service_to_encrypt=service_to_encrypt,
    #         port_to_encrypt=port_to_encrypt
    #     )
    # os.system(ansible_cmd)
    # os.system("git restore hosts")

def do_letsencrypt(
    user,
    host,
    domain,
    email,
    service_to_encrypt,
    port_to_encrypt,
    test_cert,
    app_name,
    django_staticfiles_directory,
    django_media_directory,
    django_max_upload_size,
    django_upload_buffer_size,
):
    pass
    # if test_cert:
    #     test_cert = "--test-cert"
    # else:
    #     test_cert = " "
    # if app_name != "":
    #     app_name_extravar = " app_name="+app_name
    # else:
    #     app_name_extravar = " "

    # # TODO: Don't handle inventory this way.
    # # replace_line_in_file(dawn_path+"/ansible/hosts", "123.123.123.123", 
    # #     host + "    ansible_python_interpreter=/usr/bin/python3")
    # os.chdir(dawn_path+"/ansible")
    # ansible_cmd = 'ansible-playbook -u {user} -i hosts \
    #     --extra-vars "domain={domain} email={email} \
    #     service_to_encrypt={service_to_encrypt} \
    #     port_to_encrypt={port_to_encrypt} test_cert={test_cert} \
    #     {app_name_extravar} \
    #     django_staticfiles_directory={django_staticfiles_directory} \
    #     django_media_directory={django_media_directory} \
    #     django_max_upload_size={django_max_upload_size} \
    #     django_upload_buffer_size={django_upload_buffer_size}" \
    #     letsencrypt.yml'.format(
    #         user=user, 
    #         domain=domain,
    #         email=email,
    #         service_to_encrypt=service_to_encrypt,
    #         port_to_encrypt=port_to_encrypt,
    #         test_cert=test_cert,
    #         app_name_extravar=app_name_extravar,
    #         django_staticfiles_directory=django_staticfiles_directory,
    #         django_media_directory=django_media_directory,
    #         django_max_upload_size=django_max_upload_size,
    #         django_upload_buffer_size=django_upload_buffer_size,
    #     )
    # os.system(ansible_cmd)
    # os.system("git restore hosts")

# def backup_dir(user, host, remote_dir, local_dest=backups_path, delete=False):
#     print("Backing up {remote_dir}...".format(remote_dir=remote_dir))
#     rsync_cmd = "rsync --recursive --no-links "
#     if delete:
#         rsync_cmd += "--delete "
#     rsync_cmd += "{user}@{host}:{remote_dir} {local_dest}/".format(
#         user=user,
#         host=host,
#         remote_dir=remote_dir,
#         local_dest=local_dest
#     )
#     proc = run(shlex.split(rsync_cmd))
#     print("... Done.")
# 
# def backup_database(
#     host,
#     path_to_ssh_key,
#     database_user,
#     database_password,
#     database_name,
#     local_dest=backups_path
# ):
#     print("Starting database backup process...")
#     proxy_process = proxy_connection(host, "dawn_db", 3306, path_to_ssh_key)
# 
#     # TODO: Test database connectivity, and don't go on until it is OK.
#     #       But for now, 7 seconds seems enough
#     #       to build up the tunnel connection.
#     sleep(7)
#     mysql_dump_output_file = open("{local_dest}/{database_name}.sql".format(
#         local_dest=local_dest,
#         database_name=database_name
#         ), "w")
#     mysql_dump_cmd = "mysqldump --user={database_user} \
#         --password={database_password} --port=9000 --host=127.0.0.1 \
#         --protocol=TCP --no-tablespaces --column-statistics=0 \
#         {database_name}".format(
#             database_user=database_user,
#             database_password=database_password,
#             database_name=database_name,
#         )
#     print("Starting mysqldump...")
#     print(mysql_dump_cmd)
#     proc = run(shlex.split(mysql_dump_cmd), stdout=mysql_dump_output_file)
#     print("... Done.")
# 
#     print("Killing proxy connection...")
#     proxy_process.kill()
#     print("... Done.")
#     mysql_dump_output_file.close()
# 
# def do_backup(
#         user,
#         host,
#         path_to_ssh_key,
#         database_user,
#         database_password,
#         database_name,
#         local_dest=backups_path,
#         delete=False
# ):
#     print("Started backup process...")
#     if not os.path.exists(local_dest):
#         os.makedirs(local_dest)
#     backup_dir(user, host, "/root/dawn_docker_volumes/ftp_data",
#         local_dest, delete)
#     backup_dir(user, host,
#         "/root/dawn_docker_volumes/wordpress_data/wp-content",
#         local_dest, delete)
#     backup_database(host, path_to_ssh_key, database_user, database_password,
#         database_name, local_dest)
#     print("Backup process finished.")

def proxy_connection(
    host,
    forwarded_host,
    remote_port,
    path_to_ssh_key="~/.ssh/id_rsa", 
    local_port=9000,
    proxy_user="proxy_user", 
    port=2222, 
):
    pass
    # print("Opening proxy connection with following SSH-command:")
    # ssh_command = "ssh -p {port} -i {path_to_ssh_key} {proxy_user}@{host} \
    #     -L {local_port}:{forwarded_host}:{remote_port}".format(
    #         host=host,
    #         forwarded_host=forwarded_host,
    #         remote_port=remote_port,
    #         local_port=local_port,
    #         proxy_user=proxy_user,
    #         port=port,
    #         path_to_ssh_key=path_to_ssh_key
    #     ) 
    # print(ssh_command)
    # try:
    #     return Popen(shlex.split(ssh_command), stdin=PIPE, stdout=PIPE,
    #         stderr=PIPE)
    # except Exception as e:
    #     return e
    

def main():

    dawn_banner = """\
             _____     __          ___   _ 
            |  __ \   /\ \        / / \ | |
            | |  | | /  \ \  /\  / /|  \| |
            | |  | |/ /\ \ \/  \/ / | . ` |
            | |__| / ____ \  /\  /  | |\  |
            |_____/_/    \_\/  \/   |_| \_|
            -------------------------------
             Docker Automatic Website Now
            -------------------------------
    """
    parser = argparse.ArgumentParser(
        prog='docksible',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(dawn_banner + """\

            Set up a dockerized website - a WordPress site or a Django app (or Redmine for issue tracking), with one single command in your terminal. 
            """),
            # To set up a WordPress site:

            # ./dawn.py \\
            # --user someuser \\
            # --host example.com  \\
            # --database-root-password s0me_r00t_p4ssw0rd \\
            # --database-user some_mysql_user \\
            # --database-password s0me_d4t4b4s3_p4ssw0rd \\
            # --database-name wordpress \\
            # --bootstrap --services \\
            # --letsencrypt --domain example.com --email you@example.com


            # To set up a Django app:
            # 
            # ./dawn.py \\
            # --user someuser \\
            # --host example.com  \\
            # --database-root-password s0me_r00t_p4ssw0rd \\
            # --database-user some_mysql_user \\
            # --database-password s0me_d4t4b4s3_p4ssw0rd \\
            # --database-name django \\
            # --bootstrap --custom-service \\
            # --service-name django \\
            # --app-name someapp \\
            # --django-app-repository git@github.com:/you/someapp \\
            # --django-app-git-branch production \\
            # --django-dockerfile-path docker/Dockerfile \\
            # --django-secret-key somes3cretkeyasdfasdfasfsadfasfd13as2df132s1f32asf \\
            # --django-secret-key-var-name DJANGO_SECRET_KEY  \\
            # --host-domain-env-var-name HOST_DOMAIN \\
            # --django-staticfiles-directory /app/someapp/staticfiles \\
            # --django-media-directory /app/someapp/media  \\
            # --letsencrypt --domain example.com --email you@example.com \\
            # --service-to-encrypt django --port-to-encrypt 8000


            # Using the SSH proxy service:

            # ssh -p 2222 proxy_user@example.com -L 9000:dawn_mysql:3306


            # Backing up your site:

            # ./dawn.py  \\
            # --user someuser \\
            # --host example.com \\
            # --database-user some_mysql_user \\
            # --database-password s0me_d4t4b4s3_p4ssw0rd \\
            # --database-name wordpress \\
            # --backup \\
            # --path-to-ssh-key /home/you/.ssh/somekey_rsa \\
            # --local-backup-dest /home/you/backups
        epilog='Work in progress...'
    )

    parser.add_argument('user')
    parser.add_argument('host')
    # TODO: Put this back in later.
    # parser.add_argument('action', choices=[
    #         'basic-docker-compose',
    #     ],
    #     default='basic-docker-compose'
    # )
    # TODO: Should be optional in the future, but for now, we need it.
    parser.add_argument('--project-dir', '-p', required=True)

    ##########################################
    # TODO Refactor this entire application! #
    ##########################################

    # parser.add_argument("-H", "--host", help="The server on which you deploy \
    #     your web service. For example: 123.123.123.123 or example.com")
    # parser.add_argument("-U", "--user", help="The user as whom you \
    #     (or rather, Ansible) will SSH into the server. For example: \
    #     root, azureuser, or ubuntu")

    # parser.add_argument("-P", "--database-root-password",
    #     default="db_root_password", help="The database root password")
    # parser.add_argument("-u", "--database-user", default="db_user",
    #     help="The database user. Used for setting up MySQL initially, and for \
    #     connecting your web app with the database.")
    # parser.add_argument("-p", "--database-password",
    #     default="db_password", help="The database password. Used for setting \
    #     up MySQL initially, and for connecting your web app with the \
    #     database.")
    # parser.add_argument("-D", "--database-name", default="db_name",
    #     help="The database password. Used for setting \
    #     up MySQL initially, and for connecting your web app with the \
    #     database.")
    # parser.add_argument("-b", "--bootstrap", action="store_true",
    #     help="Pass this flag if you have a brand new and fresh server. This \
    #     flag will install Docker Compose on your server, so that you can \
    #     install the other services supported by this script.")
    # parser.add_argument("-s", "--services", action="store_true",
    #     help="This flag will set up a WordPress site, along with some \
    #     ancillary services, like phpMyAdmin, an SSH proxy for port \
    #     forwarding, and hidden IRC and FTP services (vestiges of some legacy \
    #     features of an older version of this script).")
    # parser.add_argument("--wp-auth-key", default="",
    #     help="This parameter is passed into WordPress' AUTH_KEY constant. If \
    #     left blank, a randomized value will be used.")
    # parser.add_argument("--wp-secure-auth-key", default="",
    #     help="This parameter is passed into WordPress' SECURE_AUTH_KEY constant. If \
    #     left blank, a randomized value will be used.")
    # parser.add_argument("--wp-logged-in-key", default="",
    #     help="This parameter is passed into WordPress' LOGGED_IN_KEY constant. If \
    #     left blank, a randomized value will be used.")
    # parser.add_argument("--wp-nonce-key", default="",
    #     help="This parameter is passed into WordPress' NONCE_KEY constant. If \
    #     left blank, a randomized value will be used.")
    # parser.add_argument("--wp-auth-salt", default="",
    #     help="This parameter is passed into WordPress' AUTH_SALT constant. If \
    #     left blank, a randomized value will be used.")
    # parser.add_argument("--wp-secure-auth-salt", default="",
    #     help="This parameter is passed into WordPress' SECURE_AUTH_SALT constant. If \
    #     left blank, a randomized value will be used.")
    # parser.add_argument("--wp-logged-in-salt", default="",
    #     help="This parameter is passed into WordPress' LOGGED_IN_SALT constant. If \
    #     left blank, a randomized value will be used.")
    # parser.add_argument("--wp-nonce-salt", default="",
    #     help="This parameter is passed into WordPress' NONCE_SALT constant. If \
    #     left blank, a randomized value will be used.")
    # parser.add_argument("-S", "--ssl-selfsigned", action="store_true",
    #     help="Pass this flag to set up a self-signed SSL certificate.")
    # # TODO: We should think about what we really want to do here.
    # #       When I first started this project, I mainly had WordPress in mind,
    # #       so that is 'baked in' together with the --services flag.
    # #       Then Redmine entered the picture and it was then the
    # #       -R, --redmine flag, and now that I need a Django installation, I
    # #       am changing it again, to -C, --custom-service.
    # #
    # #       It would be cool if we could specify something like --wordpress,
    # #       --redmine, --django, --irc, etc., but that would require some
    # #       serious wrangling of docker-compose files, which would all be
    # #       rather clunky. It would also be reinventing the PaaS wheel.
    # #
    # #       For the scope of this project, perhaps just implement some
    # #       ready-to-go, prepackaged environments, WordPress, Django and
    # #       Redmine being good examples. Other stuff, like IRC or FTP may or
    # #       may not be hard coded, depending on what I want to do. To truly be
    # #       able to customize your cloud services would likely be beyond the
    # #       scope of this project, you'd need a real PaaS project for that.
    # parser.add_argument("-C", "--custom-service", action="store_true",
    #     help="Pass this flag to set up a custom service, instead of \
    #     WordPress. Currently, Django apps and Redmine instances (for issue \
    #     tracking) are supported. You need to specify that with the \
    #     --service-name flag. See the help section of that parameter for \
    #     more info.")
    # parser.add_argument("-n", "--service-name", choices=["django", "redmine"],
    #     help="Used along with the --custom-service flag. This parameter \
    #     specifies what type of custom service you'll deploy. Currently, \
    #     django and redmine are supported.")
    # parser.add_argument("-a", "--app-name", default="", help="If you are \
    #     deploying a Django app, you must pass this parameter as well, to \
    #     specify the app name. It's the root directory of your Django project, \
    #     where the entire code lives; likely the same as the repository name.")
    # parser.add_argument("-R", "--django-app-repository", default="",
    #     help="If you are deploying a Django app, you must pass this parameter \
    #     as well, to specify which repository Ansible should clone in order to \
    #     subsequently build the Docker image from that. Examples: \
    #     https://github.com/example-user/example-app, or \
    #     git@github.com:/example-user/example-app. Obviously, your Django \
    #     app needs to be dockerized. Also, Ansible needs to be able to read \
    #     your repository. If cloning via HTTPS, this should not be a problem. \
    #     If cloning via SSH, you need to load the private SSH key for your \
    #     Git-host account onto your server and edit the remote user's \
    #     ~/.ssh/config  to specify that the Host github.com, or whatever you \
    #     use, uses your private key in the IdentityFile setting. Finally, you \
    #     need to connect once to your Git-host account with SSH, otherwise \
    #     Ansible will be stuck forever in \
    #     the fingerprint verification question.")
    # parser.add_argument("-g", "--django-app-git-branch", default="production",
    #     help="If you are deploying a Django app, use this parameter to \
    #     specify which Git branch Ansible should checkout in order to build \
    #     the Docker image. If this parameter is left blank, the default value \
    #     'production' is used.")
    # parser.add_argument("-j", "--django-dockerfile-path",
    #     default="Dockerfile", help="If you are deploying a Django app, use \
    #     this parameter to specify the path in your repository in which the \
    #     Dockerfile is found. If left blank, the default value of 'Dockerfile' \
    #     is used, meaning that the Dockerfile is located in the root of your \
    #     repository.")
    # parser.add_argument("-k", "--django-secret-key",
    #     default="django-insecure--nmneuq-s^zj%y0ydmb*w9926)p_oc6&0u=7%xx(t*h43j+j8c",
    #     help="If you are deploying a Django app, pass this parameter to \
    #     specify the value of Django's SECRET_KEY variable. This value is \
    #     written to an environment variable (see help for the next flag), \
    #     which you should read from in your app's settings.py file. If left \
    #     blank, an insecure default value, provided by Django, will be used. \
    #     Make sure to pass this flag in production settings!")
    # parser.add_argument("-K", "--django-secret-key-var-name",
    #     default="DJANGO_SECRET_KEY", help="If you are deploying a Django app, \
    #     you use the previous flag to specify the value of your app's \
    #     SECRET_KEY variable. That value is written to an environment \
    #     variable. Use this flag to specify the name of that environment \
    #     variable, as used in your code. In your app's settings.py file, you \
    #     should have a line similar to: \
    #     SECRET_KEY = os.getenv('DJANGO_SECRET_KEY'). If left blank, the \
    #     default value of 'DJANGO_SECRET_KEY' is used.")
    # parser.add_argument("-o", "--host-domain-env-var-name",
    #     default="HOST_DOMAIN", help="In your Django app's settings.py file, \
    #     you have the option to set the CSRF_TRUSTED_ORIGINS variable, in a \
    #     manner such as: CSRF_TRUSTED_ORIGINS = ['https://*.example.com'], or \
    #     CSRF_TRUSTED_ORIGINS = ['https://*.*'] (insecure), or \
    #     CSRF_TRUSTED_ORIGINS = ['https://*.' + os.getenv('HOST_DOMAIN')] (recommended). \
    #     Passing an environment variable is recommended in dockerized \
    #     situations. Use this flag to specify the name of that environment \
    #     variable.")
    # parser.add_argument("-T", "--django-staticfiles-directory", help="If you \
    #     are deploying a Django app, then Docker Compose will create a Docker \
    #     volume to host your app's staticfiles (JavaScript and CSS). This \
    #     volume is mounted into both your app's container and into the \
    #     container of the Nginx webserver. That way, Nginx can find your app's \
    #     static files, and serve them as well. For this to work, Docker \
    #     Compose needs to know the file path within your app's Docker \
    #     container, in which the static files are located. Inspect your Docker \
    #     container's internal directory tree to determine the appropriate \
    #     value of this parameter. If left blank, the default value of \
    #     '/app/APP_NAME/staticfiles' is used, where APP_NAME is the value \
    #     which you passed with the --app-name parameter. This would mean that \
    #     in your Docker container, your Django app is located inside a \
    #     directory called 'app/', and that in your Django app's root \
    #     directory, there's a directory called 'staticfiles', and inside of \
    #     that are the CSS and JavaScript files.")
    # parser.add_argument("-m", "--django-media-directory", help="If you \
    #     are deploying a Django app, then Docker Compose will create a Docker \
    #     volume to host your app's media files (uploaded images). This \
    #     volume is mounted into both your app's container and into the \
    #     container of the Nginx webserver. That way, Nginx can find your app's \
    #     media files, and serve them as well. For this to work, Docker \
    #     Compose needs to know the file path within your app's Docker \
    #     container, in which the media files are located. Inspect your Docker \
    #     container's internal directory tree to determine the appropriate \
    #     value of this parameter. If left blank, the default value of \
    #     '/app/APP_NAME/media' is used, where APP_NAME is the value \
    #     which you passed with the --app-name parameter. This would mean that \
    #     in your Docker container, your Django app is located inside a \
    #     directory called 'app/', and that in your Django app's root \
    #     directory, there's a directory called 'media', and inside of \
    #     that are the media files.")
    # parser.add_argument("-A", "--django-max-upload-size", default="5m",
    #     help="If you are deploying a Django app, use this parameter to \
    #     specify the max upload size of files uploaded by users. This \
    #     parameter is passed into Nginx's client_max_body_size setting.")
    # parser.add_argument("-F", "--django-upload-buffer-size", default="16k",
    #     help="If you are deploying a Django app, use this parameter to \
    #     specify the max buffer size of files uploaded by users. This \
    #     parameter is passed into Nginx's client_body_buffer_size setting.")
    # parser.add_argument("-l", "--letsencrypt", action="store_true",
    #     help="Pass this flag to run the Certbot container to fetch an SSL \
    #     certificate from Let's Encrypt, and to reconfigure Nginx to use \
    #     HTTPS.")
    # parser.add_argument("-t", "--test-cert", action="store_true",
    #     help="If you use --letsencrypt to get an SSL certificate, then pass \
    #     this flag if you only want to get a test certificate. This is helpful \
    #     for troubleshooting, when you don't want to exhaust your rate limit \
    #     on Let's Encrypt's servers.")
    # parser.add_argument("-B", "--backup", action="store_true",
    #     help="Pass this flag to download a backup of your web app's data to \
    #     your local machine. This does a number of things. It will use rsync \
    #     to attempt to download the contents of your WordPress site's \
    #     wp-content/ directory and your FTP container's data directory. It \
    #     will also open an SSH-tunnel with your SSH-proxy-service on port 2222 \
    #     and port forward your hidden MySQL service to your local machine, \
    #     from which it will pull a mysqldump, which it will write to a file of \
    #     your choosing.")
    # parser.add_argument("-E", "--delete-in-rsync", action="store_true",
    #     help="When doing a backup with the --backup flag, then if this flag \
    #     is passed, the rsync command will run with the --delete flag, which \
    #     will delete files from your local directory that are not present on \
    #     your remote server. Use this if you want to get rid of obsolete files \
    #     in your local backups.")
    # parser.add_argument("-i", "--path-to-ssh-key", default=home+"/.ssh/id_rsa",
    #     help="When doing a backup with the --backup flag, an SSH connection \
    #     opened with the SSH-proxy-service. For that, you need to use this \
    #     parameter to specify which SSH-key to use. The default value is \
    #     '.ssh/id_rsa' relative to your current user's home directory.")
    # parser.add_argument("-L", "--local-backup-dest", default=backups_path,
    #     help="When doing a backup with the --backup flag, use this parameter \
    #     to specify where on your local filesystem you want to write the files \
    #     of your backup. An rsync of your WordPress site's wp-content/ and \
    #     your FTP service's data directory, along with a mysqldump of your \
    #     database will be written there. If the directory does not exist, it \
    #     will be created. If this parameter is not passed, the default value \
    #     of 'backups/', relative to your current user's home directory, will \
    #     be used.")
    # parser.add_argument("-d", "--domain", default="", help="Use this flag to \
    #     specify the domain for which you will get an SSL-certificate from \
    #     Let's Encrypt, when using the --letsencrypt flag. In Django apps, \
    #     this flag is also passed into an environment variable (see help for \
    #     --host-domain-env-var-name flag), which your Django app can pass into \
    #     the CSRF_TRUSTED_ORIGINS variable in your settings.py file.")
    # parser.add_argument("-e", "--email", help="When getting an \
    #     SSL-certificate from Let's Encrypt with the --letsencrypt flag, use \
    #     this flag to specify the email address that you give to \
    #     Let's Encrypt.")
    # parser.add_argument("--service-to-encrypt", default="wordpress",
    #     choices=["wordpress", "django", "redmine"],
    #     help="When using --letsencrypt, Nginx needs to know which Docker \
    #     container to proxy connections to. This flag gives Nginx that \
    #     information. Possible options are 'wordpress', 'django', or \
    #     'redmine'. If left blank, the default option of 'wordpress' will be used.")
    # parser.add_argument("--port-to-encrypt", default="80",
    #     help="When using --letsencrypt, Nginx needs to know on which port \
    #     in your internal Docker network your app container can be reached. \
    #     Dawn manages WordPress sites out of the box, and they are available \
    #     on port 80. If you are using Redmine, Dawn will pull the image from \
    #     Docker Hub, which is currently set to listen on port 3000. If you are \
    #     deploying a Django app, it will depend on how you build your Docker \
    #     image, but it will likely be port 8000. If left blank, the default \
    #     value of 80 will be used, which assumes a WordPress site.")


    args = parser.parse_args()

    print(dawn_banner)

    private_data_dir = init_private_data_dir()

    rc = RunnerConfig(
        private_data_dir=private_data_dir,
        project_dir=args.project_dir,
        inventory=prepare_inventory(args.user, args.host),
        # TODO: Something like this would be the better way to do this.
        # Not only should we take it from Lampsible, but we should write
        # some small library for this type of stuff, and then use that in
        # Lampsible and in this application as well.
        # project_dir=init_project_dir(),

        # TODO: Improve this.
        playbook='basic-docker-compose.yml'
    )

    rc.prepare()
    r = Runner(config=rc)
    r.run()

    cleanup_private_data_dir(private_data_dir)

    return 0

    ##########################################
    # TODO Refactor this entire application! #
    ##########################################

    # if not os.path.isfile(
    #     home+"/ansible-playbooks/docker_ubuntu1804/playbook.yml"
    # ):
    #     print("Could not find required Ansible playbooks! Clone Git repository from https://github.com/saint-hilaire/ansible-playbooks (forked from Digital Ocean, https://github.com/do-community/ansible-playbooks)?")
    #     clone_ansible_repo_yes_no = ""
    #     while clone_ansible_repo_yes_no != "yes" and \
    #         clone_ansible_repo_yes_no != "no":
    #         clone_ansible_repo_yes_no = input("Enter 'yes' to download and continue, or 'no' to cancel: ").lower()
    #     if clone_ansible_repo_yes_no == "yes":
    #         os.chdir(home)
    #         print("Cloning from https://github.com/saint-hilaire/ansible-playbooks.git into " +
    #             home
    #         )
    #         os.system("git clone https://github.com/saint-hilaire/ansible-playbooks.git")
    #     else:
    #         exit("Aborting!")


    # if not (args.bootstrap or args.services or args.ssl_selfsigned
    #     or args.letsencrypt or args.custom_service or args.backup
    # ):
    #     exit("Please specify an action (--bootstrap, --services, \
    #         --custom-service, --ssl-selfsigned and/or --letsencrypt)")

    # # Checking for required arguments
    # if args.host is None or args.user is None:
    #     exit("Please specify a host and a user.")

    # if args.database_root_password == "db_root_password":
    #     print("WARNING! Using default value for database root password: \
    #         'db_root_password'! This is unsafe in production environments!")
    # if args.database_user == "db_user":
    #     print("WARNING! Using default value for database user: 'db_user'! \
    #         This is unsafe in production environments!")
    # if args.database_password == "db_password":
    #     print("WARNING! Using default value for database password: \
    #         'db_password'! This is unsafe in production environments!")
    # if args.database_name == "db_name":
    #     print("WARNING! Using default value for database name: 'db_name'! \
    #         This is unsafe in production environments!")

    # if args.custom_service and args.service_name is None:
    #     exit("Please specify a service name (--service-name[redmine|django])")
    # elif args.service_name == "django" and \
    #     (args.app_name == "" or args.django_app_repository == ""):
    #     exit("Please specify a name and repository for your Django app with \
    #         the --app-name --django-app-repository flags")

    # if args.service_name == "django" and \
    #     args.django_secret_key == "django-insecure--nmneuq-s^zj%y0ydmb*w9926)p_oc6&0u=7%xx(t*h43j+j8c":
    #     print("WARNING: Using default value for --django-secret-key! This is insecure for production environments!")

    # if args.django_staticfiles_directory is None:
    #     args.django_staticfiles_directory = "/app/" + args.app_name + "/staticfiles"
    # if args.django_media_directory is None:
    #     args.django_media_directory = "/app/" + args.app_name + "/media"

    # wordpress_secure_args = {
    #     "wp_auth_key"        : args.wp_auth_key,
    #     "wp_secure_auth_key" : args.wp_secure_auth_key,
    #     "wp_logged_in_key"   : args.wp_logged_in_key,
    #     "wp_nonce_key"       : args.wp_nonce_key,
    #     "wp_auth_salt"       : args.wp_auth_salt,
    #     "wp_secure_auth_salt": args.wp_secure_auth_salt,
    #     "wp_logged_in_salt"  : args.wp_logged_in_salt,
    #     "wp_nonce_salt"      : args.wp_nonce_salt,
    # }
    # for key, val in wordpress_secure_args.items():
    #     if wordpress_secure_args[key] == "":
    #         wordpress_secure_args[key] = token_hex(64)


    # if args.bootstrap:
    #     do_bootstrap(args.user, args.host)
    # if args.services:
    #     do_services(
    #         args.user,
    #         args.host,
    #         args.database_root_password,
    #         args.database_user,
    #         args.database_password,
    #         args.database_name,
    #         wordpress_secure_args['wp_auth_key'],
    #         wordpress_secure_args['wp_secure_auth_key'],
    #         wordpress_secure_args['wp_logged_in_key'],
    #         wordpress_secure_args['wp_nonce_key'],
    #         wordpress_secure_args['wp_auth_salt'],
    #         wordpress_secure_args['wp_secure_auth_salt'],
    #         wordpress_secure_args['wp_logged_in_salt'],
    #         wordpress_secure_args['wp_nonce_salt']
    #     )
    # if args.custom_service:
    #     do_custom_service(
    #         args.user,
    #         args.host,
    #         args.domain,
    #         args.database_root_password,
    #         args.database_user,
    #         args.database_password,
    #         args.database_name,
    #         args.service_name,
    #         args.app_name,
    #         args.django_app_repository,
    #         args.django_app_git_branch,
    #         args.django_dockerfile_path,
    #         args.django_secret_key,
    #         args.django_secret_key_var_name,
    #         args.host_domain_env_var_name,
    #         args.django_staticfiles_directory,
    #         args.django_media_directory,
    #         args.django_max_upload_size,
    #         args.django_upload_buffer_size,
    #     )
    # if args.ssl_selfsigned:
    #     do_ssl_selfsigned(
    #         args.user,
    #         args.host,
    #         args.service_to_encrypt,
    #         args.port_to_encrypt,
    #     )
    # if args.letsencrypt:
    #     do_letsencrypt(
    #         args.user,
    #         args.host,
    #         args.domain,
    #         args.email,
    #         args.service_to_encrypt,
    #         args.port_to_encrypt,
    #         args.test_cert,
    #         args.app_name,
    #         args.django_staticfiles_directory,
    #         args.django_media_directory,
    #         args.django_max_upload_size,
    #         args.django_upload_buffer_size,
    #     )
    # if args.backup:
    #     do_backup(
    #         args.user,
    #         args.host,
    #         args.path_to_ssh_key,
    #         args.database_user,
    #         args.database_password,
    #         args.database_name,
    #         args.local_backup_dest,
    #         args.delete_in_rsync
    #     )

if __name__ == "__main__":
    main()
