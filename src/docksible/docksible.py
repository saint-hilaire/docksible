import os
import argparse

# TODO: Won't need this, after we have "The Library".
from sys import path as sys_path

from getpass import getpass
from ansible_runner import Runner, RunnerConfig

# Shouldn't need these.
# import shlex
# from subprocess import run, Popen, PIPE
# from time import sleep

from secrets import token_hex

# TODO: This will need to be improved!
# I copy-pasted from another project, but I want to that stuff
# in a dedicated library - that's what the other comments
# about "The Library" are about.
from docksible.constants import *
from docksible.arg_validator import ArgValidator

__author__ = "Brian St. Hilailre"
__copyright__ = "Copyright 2022, Sanctus Technologies UG (haftungsb.)"
__license__ = "Apache License, Version 2.0"
__version__ = "0.2"
__maintainer__ = "Brian St. Hilaire"
__email__ = "brian.st-hilaire@sanctus-tech.com"


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


# TODO: Copy-pasted from Lampsible.
# We need "The Library" for stuff like this.
def init_project_dir(project_dir):
    if project_dir == '':
        return find_package_project_dir()
    return project_dir


def find_package_project_dir():
    for path_str in sys_path:
        try:
            try_path = os.path.join(path_str, 'docksible', 'project')
            assert os.path.isdir(try_path)
            return try_path
        except AssertionError:
            pass
    raise RuntimeError("Got no user supplied --project-dir, and could not find one in expected package location. Your Docksible installation is likely broken. However, if you are running this code directly from source, this is expected behavior. You probably forgot to pass the '--project-dir' flag. The directoy you're looking for is 'src/docksible/project/'.")


# TODO: Refactor this into the library - see Lampsible.
# Obviously, improve this!
def cleanup_private_data_dir(path):
    os.system('rm -r ' + path)


# TODO: Copypasted from Lampsible. This also belongs in "The Library".
def get_pass_and_check(prompt, min_length):
    password = getpass(prompt)
    while len(password) < min_length:
        password = getpass('That password is too short. Please enter another password: ')
    double_check = getpass('Please retype password: ')
    if password == double_check:
        return password
    else:
        print('Passwords don\'t match. Please try again.')
        return get_pass_and_check(prompt, min_length)


# This is basically WordPress, and also IRC and FTP on the side...
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

    parser = argparse.ArgumentParser(
        prog='docksible',
        # formatter_class=argparse.RawDescriptionHelpFormatter,
        # description=textwrap.dedent(dawn_banner + """\

        #     Set up a dockerized website - a WordPress site or a Django app (or Redmine for issue tracking), with one single command in your terminal. 
        #     """),
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

    parser.add_argument('user', help="The user as whom you \
        (or rather, Ansible) will SSH into the server. For example: \
        root, azureuser, etc.")
    parser.add_argument('host', help="The server on which you deploy \
        your web service. For example: 123.123.123.123 or example.com")
    parser.add_argument('action', choices=[
        'setup-docker-compose',
        'wordpress',
        'redmine',
        'osem',
    ])

    parser.add_argument('--ask-remote-sudo', action='store_true')
    parser.add_argument('--insecure-cli-password', action='store_true')
    parser.add_argument('--remote-sudo-password')
    parser.add_argument('--database-root-password')
    parser.add_argument('--database-username')
    parser.add_argument('--database-password')
    parser.add_argument('--database-name')
    parser.add_argument('--database-table-prefix')
    parser.add_argument('--letsencrypt', '-l', action='store_true')
    parser.add_argument('--domain', '-d')
    parser.add_argument('--email',  '-e')
    parser.add_argument('--test-cert', '-t', action='store_true')

    parser.add_argument('--project-dir', '-p', default='')

    args = parser.parse_args()

    validator = ArgValidator(args)
    if validator.validate_args() != 0:
        print('FATAL! Bad args')
        return 1
    args = validator.get_args()


    private_data_dir = init_private_data_dir()
    project_dir = init_project_dir(args.project_dir)
    inventory = prepare_inventory(args.user, args.host)
    
    # TODO: Improve this validation - this is just rudimentary.
    # if args.action == 'redmine':
    #     database_root_password = get_pass_and_check(
    #         'Please enter a database root password',
    #         7
    #     )
    # else:
    #     database_root_password = None

    playbook = '{}.yml'.format(args.action)

    extravars = {
        'database_root_password': args.database_root_password,
        'database_username': args.database_username,
        'database_password': args.database_password,
        'database_name': args.database_name,
        # TODO: This is an antipattern. Normally this variable would
        # be supplied by Ansible, but we're not doing inventories
        # completely the right way, which would be a little tricky.
        # (So ansible_host equals 'user@server' when I just want it to be
        # 'server')
        # See the large essay I wrote in the comment in the function
        # prepare_inventory in Lampsible.
        'server_name': args.host,
    }

    if args.action == 'wordpress':
        extravars['wordpress_auth_vars'] = validator.get_wordpress_auth_vars()

    if args.action == 'osem':
        extravars['osem_secret_key_base'] = token_hex(64)

    rc = RunnerConfig(
        private_data_dir=private_data_dir,
        project_dir=project_dir,
        inventory=inventory,
        # TODO: Something like this would be the better way to do this.
        # Not only should we take it from Lampsible, but we should write
        # some small library for this type of stuff, and then use that in
        # Lampsible and in this application as well.
        # project_dir=init_project_dir(),

        # TODO: Improve this.
        playbook=playbook,
        extravars=extravars
    )

    rc.prepare()
    r = Runner(config=rc)
    r.run()

    if args.letsencrypt:

        # TODO: Validation...
        if args.domain is None:
            args.domain = args.host

        while args.email is None:
            args.email = input('Please enter an email address: ')

        # TODO: This is very rudimentary! In the future, we shouldn't
        # need to run a second play for this. Instead, do it all in one go.

        if args.action == 'redmine' or args.action == 'osem':
            port_to_encrypt = '3000'
        else:
            port_to_encrypt = '80'

        rc = RunnerConfig(
            private_data_dir=private_data_dir,
            project_dir=project_dir,
            inventory=inventory,
            # TODO: Something like this would be the better way to do this.
            # Not only should we take it from Lampsible, but we should write
            # some small library for this type of stuff, and then use that in
            # Lampsible and in this application as well.
            # project_dir=init_project_dir(),

            # TODO: Improve this.
            playbook='letsencrypt.yml',
            extravars={
                'domain': args.domain,
                'email':  args.email,
                'service_to_encrypt': args.action,
                'port_to_encrypt':    port_to_encrypt,
                'test_cert': '--test-cert' if args.test_cert else ' ',
            }
        )

        rc.prepare()
        r = Runner(config=rc)
        r.run()

    cleanup_private_data_dir(private_data_dir)

    return 0

    # if args.ssl_selfsigned:
    #     do_ssl_selfsigned(
    #         args.user,
    #         args.host,
    #         args.service_to_encrypt,
    #         args.port_to_encrypt,
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
