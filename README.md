# Docksible

## About

This is a tool you can run locally to install a given web app via Docker Compose onto a remote VPS.
Though not recommended for serious enterprise grade production environments, it is well suited
to quickly spin up an off the cuff demo server, or even a small production server.

## Features

* WordPress
* Redmine (open source issue tracker)
* SSL
* Hopefully more soon ;-)

## Requirements

* Local: Unix with Python 3.11 or newer. Tested this on Gentoo and Ubuntu Linux.
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
