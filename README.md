Get a VPS, for example AWS or Digital Ocean.   
The VPS needs ports 22 and 2222 open.   
Note the user and public IP address (or domain name) of that server, then run the deployment script:   
`./dawn.py -u <USER> -H <HOST>`
That command will install Docker and Docker Compose onto the server, and set up the needed containers over there.

There is a little bit of manual stuff that you need to do on the server:
Set up a user for new people, where they can log in with a password that we give them, and copy their keys.
This is on the SSH server **on the host**.
Switch the SSH configurations to allow/disallow passwords as needed, in `/etc/ssh/sshd_config`


The deployment script will pull in the repository for the SSH-proxy, and in there, you should have a 
directory into which you can copy the `authorized_keys` file, onto which the users will copy their keys, into.
That should leave you with something like this:
`$HOME/dawn_docker_volumes/ssh-proxy_data/authorized_keys`

**TODO:** We have to manually fix the permissions of the `authorized_keys` file in the container, but fortunately, we only have to do this the first time.
`docker exec -it dawn_ssh-proxy bash`
`chown proxy_user:proxy_user /home/proxy_user/.ssh/authorized_keys`



On your local machine, do this:
`ssh -i /home/user/.ssh/private_key -p 2222 -L <LOCAL_PORT>:dawn_ircd:6667 proxy_user@123.123.123.123`, where `<LOCAL_PORT>` is a port that you choose,  such as 9000, then you can connect to the IRC server with your favorite IRC client on `localhost:<LOCAL_PORT>`
