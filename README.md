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

