# Docksible

## About

This is a tool you can run locally to install a given web app via Docker Compose onto a remote VPS.
Though not recommended for serious enterprise grade production environments, it is well suited
to quickly spin up an off the cuff demo server, or even a small production server.

### Warning

This tool is still under development and not stable yet.
Until version 1.0 becomes available, things can and will break between releases.

## Features

* WordPress
* Redmine (open source issue tracker)
* SSL
* SSH proxy to tunnel hidden services like database
* Hopefully more soon ;-)

## Requirements

* Local: Unix with Python 3.9 or newer. Tested this on Gentoo and Ubuntu Linux.
  Might work on macOS, but I don't know. Won't work on Windows, because it uses
  Ansible under the hood, which AFAIK is not supported for Windows.
* Remote: VPS running Ubuntu, or maybe other Debian based flavor, reachable via SSH.
  It should probably work on all Debian distros, but I have only tested on Ubuntu.

## Installing

Intall with Pip: `python -m pip install docksible`

## Usage

These examples should be self explanatory:

* `docksible user@example.com wordpress --letsencrypt --email admin@example.com`
* `docksible user@example.com redmine --letsencrypt --email admin@example.com`

Run the `--help` flag for all supported options.

### Using the SSH proxy

You can include a [simple SSH proxy](https://github.com/saint-hilaire/simple-ssh-proxy)
into your app's Docker network, by passing the `--ssh-proxy` flag. This will drop in
a small container that you can use to port forward some hidden services, like the
database. Here's how to do it:

* Include `--ssh-proxy` in the Docksible command (ex: `docksible user@host wordpress --ssh-proxy`)
* Set up the proxy service's `authorized_keys` file. This will be improved in the future,
  but until then:
  * SSH into your server as root
  * Copy root's `.ssh/authorized_keys` into `docksible-volumes/ssh-proxy-data/`
  * Shell into the proxy container, and basically `chown -R proxy_user:proxy_user /home/proxy_user`.
    This could also be improved, but for now, just needs to be done once.
* Now the proxy service is ready to use. For example:
  * Set up the tunnel to proxy the database:
  ```
  ssh -p 2222 proxy_user@yourserver.com -L 9000:docksible_db:3306
  ```
  * Connect to the database:
  ```
  mysql -u your_db_user -p --port=9000 --host=localhost --protocol=TCP
  ```

## Known issues

When setting up a web app on Ubuntu 24.10 and newer, and doing so with the
`--letsencrypt` flag, which is recommended, you must also set the
`--apparmor-workaround` flag.

This because it seems that in Ubuntu 24.10 and newer,
there is an issue with AppArmor that prevents Docker containers from being
restarted, even when doing so as root, which occurs a few times in the
Let's Encrypt role.

Setting the flag `--apparmor-workaround` will result in the raw command
`aa-remove-unknown` being run on the server everytime before a container
gets restarted. This workaround fixes the issue for now, but it is not
elegant. Doing this on older versions results in a different error,
hence the CLI option.

Altogether, it's tech debt, a temporary workaround, and will be removed soon.
Also, the Let's Encrypt handling will be refactored and improved altogether.
See these issues for more info:

* https://github.com/saint-hilaire/docksible/issues/27
* https://github.com/saint-hilaire/docksible/issues/24

