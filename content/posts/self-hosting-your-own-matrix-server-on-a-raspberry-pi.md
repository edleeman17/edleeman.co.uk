---
title: "Self Hosting Your Own Matrix Server on a Raspberry Pi"
date: 2021-07-02T19:39:30Z
draft: false
type: post
---

## What is Matrix?

"Matrix is an open source project that publishes the [Matrix open standard](https://matrix.org/docs/spec) for secure, decentralised, real-time communication, and its Apache licensed [reference implementations](https://github.com/matrix-org). Maintained by the non-profit [Matrix.org Foundation](https://matrix.org/foundation/), we aim to create an open platform which is as independent, vibrant and evolving as the Web itself... but for communication. As of June 2019, Matrix is [out of beta](https://matrix.org/blog/2019/06/11/introducing-matrix-1-0-and-the-matrix-org-foundation), and the protocol is fully suitable for production usage." ~ [matrix.org](https://matrix.org/)

## Self-hosting Synapse (Matrix)

### Prerequisites

There are a few assumptions that need to be made before we can start:

- You own either a [Raspberry Pi](https://amzn.to/3qHO1ZY) or have a server available (maybe [Digital Ocean](https://m.do.co/c/d2a3afe52625)?)
- A Domain Name
- Access to your DNS records
- General knowledge of Portforwarding

### Step 1: Installing Docker on your server

All of the following instructions are based on the Debian distro, so if you're running a server with Ubuntu, these instructions will be perfect for you. If not, you may have to adjust the commands below to suit your distro.

The first step is to just make sure our server is up to date. Run the following commands to pull down the latest updates from our distro repositories.

    sudo apt-get update && sudo apt-get upgrade

You should see an output like the following
![Console output for running update and upgrade commands](https://theselfhostingblog.com/content/images/2021/02/image-7.png)Console output for running the update and upgrade commands
Next, we need to install Docker. Docker is the layer which your containers run.

To install Docker on your instance, you need to run the following command.

The following script is a convenience script [**provided by the Docker team**](https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script). It's highly recommended to always check what you're going to execute, before executing it.

    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh

Installing Docker using the convenience script
Once you have executed the Docker install script. You should see an output like the following.
![Docker convenience script install output](https://theselfhostingblog.com/content/images/2021/02/image-8.png)Docker convenience script install output
As you can see in the output, the command was executed successfully. You may also notice that there is a console message specifying how to use Docker as a non-root user.

This means that whenever you are executing the Docker command, you'll no longer need to type in your sudo password.

If this sounds good to you, you can simply run the provided command, substituting `your-user` for your server user. In my case, my user is `ubuntu`. My command would look like this.

    sudo usermod -aG docker ubuntu

Adding your user to the Docker group
We also need to install Docker Compose. This can be done by running the following commands.

    sudo curl -L "https://github.com/docker/compose/releases/download/1.28.5/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

### Step 2: Synapse Configuration

Now that we have Docker and Docker Compose installed, we can begin to create our Synapse server.

First thing we need is a `docker-compose.yml` file. I like to put this in its own folder.

It doesn't really matter where your folder lives, but I'm going to add mine into my home directory.

    cd
    mkdir matrix
    cd matrix

Now, we can create our `docker-compose.yml`

    nano docker-compose.yml

Paste in the following, it should be everything that you need.

    version: '3.3'

    services:
      app:
        image: matrixdotorg/synapse
        restart: always
        ports:
          - 8008:8008
        volumes:
          - /var/docker_data/matrix:/data

Save and exit your `docker-compose.yml`

We now need to generate our homeserver configuration file.

Run the following command, replacing `YOUR_DOMAIN` with your actual domain name.

It's recommended to set up Matrix on a sub-domain. You can do this by setting up an A Record in your DNS config that points to your External IP address.

    docker run -it --rm -v /var/docker_data/matrix:/data -e SYNAPSE_SERVER_NAME=matrix.YOUR_DOMAIN -e SYNAPSE_REPORT_STATS=yes matrixdotorg/synapse:latest generate

This will generate a new config file at `/var/docker_data/matrix/homeserver.yaml` which we will use later to enable user registration.

We can now start our Synapse server.

    docker-compose up -d

Once running, you can navigate to your IP address on port 8008; e.g `192.168.1.5:8008`

You should see something that looks like the following
![](https://theselfhostingblog.com/content/images/2021/07/image.png)
Cool, so that's working locally. But what use is that? we want to talk to people right? We need to expose our new service to the web!

We're going to use Nginx in this tutorial.

### Step 3: Installing and configuring Nginx

Nginx is a reverse proxy that allows us to point a domain name to our Papercups service. By default, Synapse will be running on port 8008.

First, we need to install Nginx.

    sudo apt-get install nginx

Once installed, we need to configure a new site. This is essentially a config file that will allow routing on a certain domain name to our Papercups service.

Usually, I name my sites by their URL. To create a new site, run the following command, substituting my URL with yours.

    sudo nano /etc/nginx/sites-available/matrix.selfhostingblog.com

This will open up a new window that allows us to add our Nginx configuration. Now, you're about to paste in a lot of text, but don't worry, I'll walk you through what we need to change.

Paste in the following code.

    server {

            server_name matrix.selfhostingblog.com;

            location / {
                    proxy_pass http://localhost:8008;
            }
    }


Most of this is configured for you and doesn't need to be changed. Only the URL which Nginx wants to use. You'll see that mine is `matrix.selfhostingblog.com` make sure that you change this to your URL. Also, don't forget the `;` at the end of the line. It'll save you a lot of headaches 😉

We now need to hit `Ctrl + x` ,`y` and `return` to save and exit out of `nano`.

Now, we just need to register our new site with Nginx, you can do this by running the following command. Again substituting my domain with yours.

    sudo ln -s /etc/nginx/sites-available/matrix.selfhostingblog.com /etc/nginx/sites-enabled/matrix.selfhostingblog.com

We just need to remove the default Nginx configuration to prevent a port clash.

    sudo rm /etc/nginx/sites-available/default
    sudo rm /etc/nginx/sites-enabled/default

Now, we can test the Nginx configuration. Run the following command.

    sudo nginx -t

Which should give us a successful output.
![](https://theselfhostingblog.com/content/images/2021/07/image-1.png)
Sweet. Let's restart the Nginx service.

    sudo systemctl restart nginx

### Step 4: Port-forwarding

If you're self-hosting this on your own hardware, you will need to port forward your instance to allow public access to your instance. This will involve googling how to port forward from your router.

You'll need to [**point port 80 and 443 to your instance**](https://portforward.com/) where Nginx is set up.

If you're hosting Synapse in Digital Ocean, you may need to configure UFW.

I have a tutorial for [**setting up UFW here**](https://theselfhostingblog.com/posts/setting-up-ufw-on-ubuntu-server/)

    sudo ufw app list

    Output
    ---

    Available applications:
      Nginx Full
      Nginx HTTP
      Nginx HTTPS
      OpenSSH

As you can see, there are three profiles available for Nginx:

- **Nginx Full**: This profile opens both port 80 (normal, unencrypted web traffic) and port 443 (TLS/SSL encrypted traffic)
- **Nginx HTTP**: This profile opens only port 80 (normal, unencrypted web traffic)
- **Nginx HTTPS**: This profile opens only port 443 (TLS/SSL encrypted traffic)

It is recommended that you enable the most restrictive profile that will still allow the traffic you’ve configured. Since we will be configuring SSL for our server we will need to temporarily allow port 80 and 443 for Certbot to verify our domain endpoint.

You can enable this by typing:

    sudo ufw allow 'Nginx Full'

### Step 5: Configuring Certbot

Certbot allows us to generate SSL certificates for free with Let's Encrypt. It's simple to install and use. Even hooks in with Nginx, meaning that there's no more manual configuration required.

To install Certbot, simply run the following commands

    sudo apt-get install certbot python3-certbot-nginx

Then, to set up your SSL certificate, run. Make sure that you have your domain name pointing to your IP address. This will require some DNS configuration. You'll need an A Record.

    sudo certbot --nginx

Follow the instructions, select your domain name from the Nginx list.
Also, select `redirect` as this will upgrade any HTTP requests to HTTPS.

You should also notice that the SSL certificate is causing your domain to be HTTPS!

### Step 6: Connecting to your new Synapse server

Now that you have everything secure, you should be able to connect to your server now.

Head over to [https://app.element.io/](https://app.element.io/) and enter your homeserver url.
![](https://theselfhostingblog.com/content/images/2021/07/image-2.png)
If everything has been configured correctly, you should be able to enter a username and password (which we haven't set up yet)
![](https://theselfhostingblog.com/content/images/2021/07/image-3.png)
We now need federation to work, so we are able to join other channels on other homeservers and chat privately other Matrix users

We're also using a subdomain to connect to matrix (matrix.selfhostingblog.com) but it would look nicer if our username looked like this: `@myuser:selfhostingblog.com` rather than `@myuser:selfhostingblog.com`.

To correct these, we need to do configure Federation.

### Step 7: Configuring Federation

We need to make some changes to our Nginx config from before.

    sudo nano /etc/nginx/sites-available/matrix.selfhostingblog.com

Here's how we currently look.

    server {

            server_name matrix.selfhostingblog.com;

            location / {
                    proxy_pass http://localhost:8008;
            }

            listen 443 ssl; # managed by Certbot
            ssl_certificate /etc/letsencrypt/live/matrix.selfhostingblog.com/fullchain.pem; # managed by Certbot
            ssl_certificate_key /etc/letsencrypt/live/matrix.selfhostingblog.com/privkey.pem; # managed by Certbot
            include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
            ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
    }


We need to add `listen 8448 ssl;` to this server block

    server {

            server_name matrix.selfhostingblog.com;

            location / {
                    proxy_pass http://localhost:8008;
            }

            listen 8448 ssl;
            listen 443 ssl; # managed by Certbot
            ssl_certificate /etc/letsencrypt/live/matrix.selfhostingblog.com/fullchain.pem; # managed by Certbot
            ssl_certificate_key /etc/letsencrypt/live/matrix.selfhostingblog.com/privkey.pem; # managed by Certbot
            include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
            ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot
    }


We also need to add a `.well-known` file. This will allow us to Federate our server and use our base domain as our identity.

    server {
            server_name selfhostingblog.com;

            location /.well-known/matrix/client {
                    return 200 '{"m.server": {"base_url": "matrix.selfhostingblog.com:443"}}';
                    default_type application/json;
                    add_header Access-Control-Allow-Origin *;
            }
    }


We'll need to run `certbot` again for this new url. Eventually, your Nginx config should look like the following.

    server {

            server_name matrix.selfhostingblog.com;

            location / {
                    proxy_pass http://localhost:8008;
            }

            listen 8448 ssl;
            listen 443 ssl; # managed by Certbot
            ssl_certificate /etc/letsencrypt/live/matrix.selfhostingblog.com/fullchain.pem; # managed by Certbot
            ssl_certificate_key /etc/letsencrypt/live/matrix.selfhostingblog.com/privkey.pem; # managed by Certbot
            include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
            ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot


    }

    server {
            server_name selfhostingblog.com;

            location /.well-known/matrix/client {
                    return 200 '{"m.server": {"base_url": "matrix.selfhostingblog.com:443"}}';
                    default_type application/json;
                    add_header Access-Control-Allow-Origin *;
            }

        listen 443 ssl; # managed by Certbot
        ssl_certificate /etc/letsencrypt/live/matrix.selfhostingblog.com/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/matrix.selfhostingblog.com/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

    }


You will now need to open up port `8448` on your router.

Then execute

    sudo systemctl restart nginx

### Step 8: Regenerating the config and creating your user

Now that we have Federation set up, we should delete the previous homeserver config and use our new domain.

    cd /var/docker_data/matrix
    sudo rm -f *

Then run the following, with your domain name (excluding `matrix.`)

    docker run -it --rm -v /var/docker_data/matrix:/data -e SYNAPSE_SERVER_NAME=selfhostingblog.com -e SYNAPSE_REPORT_STATS=yes matrixdotorg/synapse:latest generate

Now let's edit the new config and enable registration

    sudo nano /var/docker_data/matrix/homeserver.yaml

Add this line

    enable_registration = true

Save and exit, and then run your docker container.

    docker-compose up -d

You should now be able to open up [https://app.element.io/#/register](https://app.element.io/#/register) on your homeserver url (https://matrix.selfhostingblog.com) and create a user.

You can also test your Federation, using the following URL [https://federationtester.matrix.org/#selfhostingblog.com](https://federationtester.matrix.org/#selfhostingblog.com)
![](https://theselfhostingblog.com/content/images/2021/07/image-4.png)
## That's it

That should be you set up. There's a lot of moving parts in this tutorial, much of it is from other tutorials on the web, but this is what worked for me on my Raspberry Pi. Let me know if you get stuck and I'll try and help you out. Thanks for reading!
This post contains affiliate links, meaning we  may receive a small commission on purchases made through links in this post. At no extra cost to you 😊

We hate Ads! They don't respect your privacy.

Would you consider supporting us on [buy me a coffee](https://www.buymeacoffee.com/selfhostingblog)? Your support really helps to keep the costs down with running the blog

