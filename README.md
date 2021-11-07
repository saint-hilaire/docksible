# DAWN - Docker Automatic Website Now

## What is this?

This is a script that you can run on your local machine to set up a dockerized website - a WordPress site or a Django app (or Redmine for issue tracking), on a given remote server, with one single command in your terminal. 
<br>
The Python wrapper script will, based on the input that you give it, run a series of Ansible playbooks, setting everything up on the server, including a Docker network, managed by Docker Compose, on which your web apps run.
<br>
The end effect is that you run a single command in your shell, watch the script run, and when it's done, your site will be running on your new server.
<br>

There are also various other features supported, such as:

- Automatic SSL certificates
- An SSH proxy to port forward your hidden services
- A hidden FTP server
- A hidden IRC server
- Command to copy your server's data to a local backup

## What is this not?

This is not a proper PaaS-tool or other infrastructure tool for serious production environments. You can use this to spin up a lightweight Django app, or some smaller clients' WordPress sites, or an off the cuff Redmine installation. It is not recommended, however, to use this in serious enterprise grade production environments

## Installing your web app.

First, you need to get a VPS, from your cloud provider of choice; this script has been tested with Digital Ocean, AWS, and OVH, but it will likely work on any other provider.
<br>
The VPS needs to run Ubuntu and you need at least Version 18.
<br>
The VPS needs to be reachable on ports 22, 80, and 443; and if you want to use SSH-proxy service for port forwarding (to connect to MySQL/phpMyAdmin, do backups, and some other cool stuff like connecting to a hidden IRC service), then you also need port 2222 open.   
<br>
If you are going to use a domain with your web app, which is highly recommended, then you need to log into your domain name registrar, and point the A records to the public IP address of your VPS. **Important:** In WordPress sites, if you are using example.com, you need to point example.com, as well as www.example.com, to your server's public IP address.

<br>

When that is all set up, you can run `dawn.py` to start your web app. For a comprehensive description of all available options, run `dawn.py --help`.

<br>

Setting up a WordPress site could look something like this:
```
./dawn.py \
--user someuser \
--host example.com  \
--database-root-password s0me_r00t_p4ssw0rd \
--database-user some_mysql_user \
--database-password s0me_d4t4b4s3_p4ssw0rd \
--database-name wordpress \
--bootstrap --services \
--letsencrypt --domain example.com --email you@example.com
```
Note: For the following parameters, you can also pass your own values. If you don't, Python will generate a randomized value and use that.
- `--wp-auth-key`
- `--wp-secure-auth-key`
- `--wp-logged-in-key`
- `--wp-nonce-key`
- `--wp-auth-salt`
- `--wp-secure-auth-salt`
- `--wp-logged-in-salt`
- `--wp-nonce-salt`


Setting up a Django app could look something like this:
```
./dawn.py \
--user someuser \
--host example.com  \
--database-root-password s0me_r00t_p4ssw0rd \
--database-user some_mysql_user \
--database-password s0me_d4t4b4s3_p4ssw0rd \
--database-name django \
--bootstrap --custom-service \
--service-name django \
--app-name someapp \
--django-app-repository git@github.com:/you/someapp \
--django-app-git-branch production \
--django-dockerfile-path docker/Dockerfile \
--django-secret-key somes3cretkeyasdfasdfasfsadfasfd13as2df132s1f32asf \
--django-secret-key-var-name DJANGO_SECRET_KEY  \
--host-domain-env-var-name HOST_DOMAIN \
--django-staticfiles-directory /app/someapp/staticfiles \
--django-media-directory /app/someapp/media  \
--letsencrypt --domain example.com --email you@example.com \
--service-to-encrypt django --port-to-encrypt 8000
```

After running all that, your site *should* be up and running. It normally works, but if something went wrong, it's usually because something happened with Certbot. Verify that your domains are properly set up, and run the command a second time; that usually does the trick. If it still isn't working, it is recommended that you troubleshoot by passing the  `--test-cert` flag (to avoid exhausting your rate limit with Let's Encrypt), and inspecting your Docker logs.

In a Django app, you will likely want to create a super user to log into the admin. To do that, log into your server, and do something like:
```
docker exec -it dawn_django python manage.py createsuperuser
```

## Using the SSH-Proxy
When your site is running, the Docker network will include a container which acts as a proxy service. You can connect to that service as the user `proxy_user` on port 2222 on your server. From there, you can port-forward some of your Docker network's hidden services to your local machine. This is useful because the included MySQL and phpMyAdmin services are not publicly exposed. To connect to them, you could do something like this:
```
ssh -p 2222 proxy_user@example.com -L 9000:dawn_mysql:3306
ssh -p 2222 proxy_user@example.com -L 9001:dawn_phpmyadmin:80
```

Then, you can connect to MySQL with `mysql --user=some_user --password --host=localhost --port=9000 --protocol=TCP`, and phpMyAdmin by navigating to localhost:9001 in a web browser.

**NOTE:** For this to work, you have to manually give the user `proxy_user` an `authorized_keys` file, and make that user into the owner of that file. See https://github.com/saint-hilaire/dawn/issues/3. You have to do something like this:
```
sudo cp ~/.ssh/authorized_keys /root/dawn_docker_volumes/ssh-proxy_data/ 
docker exec  -it dawn_ssh-proxy bash
chown -R proxy_user /home/proxy_user/
```
You only have to do this once initially.


## Making Backups
You can make a local backup of your site's data with a single command. This requires that the SSH-proxy is set up and working (see previous section). Doing a backup of a WordPress site, which saves a MySQL-Dump of the database, along with the contents of your site's `wp-content/` directory to your local computer, would look something like this:
```
./dawn.py  \
--user someuser \
--host example.com \
--database-user some_mysql_user \
--database-password s0me_d4t4b4s3_p4ssw0rd \
--database-name wordpress \
--backup \
--path-to-ssh-key /home/you/.ssh/somekey_rsa \
--local-backup-dest /home/you/backups/directory-for-your-site
```



## Note for Certbot

In case Certbot failed, for whatever reason, you can still do it manually:    

- Edit `dawn_docker_volumes/nginx_data/nginx.conf`, get rid of the line that tells the server to listen on port 443, and to use any SSL certificates. Also copy the block `location ~ /.well-known` to the server block for port 80.
- Restart Nginx with `docker-compose -f docker-compose-certbot.yml restart dawn_webserver`
- Verify that Nginx is running with `docker ps`
- Run the Certbot container with `docker-compose -f docker-compose-certbot.yml up dawn_certbot`
- Go back into `dawn_docker_volumes/nginx_data/nginx.conf` and reenable the configurations for port 443 and the SSL certificates. See the file `nginx.conf.j2` in the template directory for the letsencrypt Ansible role for more info.
- Restart Nginx one more time with the same command as before.


## Note for Redmine

Redmine is very feature-rich, and provides/requires extensive configuration.   
The Docker image omits much of this configuration.   
So to make future-installations easier, I have provided some sensible default configurations.   
Just connect to the database as (probably) `root:root_password`. (Or whatever you provided as the `--database-root-password`). and import `redmine_defaults.sql`.    
That configuration has some sensible defaults set up, including the following users:
- admin:adminadmin
- developer:password
- manager:password
