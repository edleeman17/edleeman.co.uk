---
title: Completely Self-Hosting Bitwarden Password Manager (Updated 2021)
slug: how-to-self-host-bitwarden-on-ubuntu-server
date: 2020-08-30T18:10:05.000Z
type: post
---



## Introduction

This article will cover setting up your own self-hosted Bitwarden instance with Docker and configuring ngnix to allow for public exposure for cross-device access to your vault.

### What is Bitwarden?

[Bitwarden ](https://bitwarden.com/)is a free and open-source password management service that stores sensitive information such as website credentials in an encrypted vault. The Bitwarden platform offers a[ variety of client applications ](https://bitwarden.com/download/)including a web interface, desktop applications, browser extensions, mobile apps, and a CLI.

Bitwarden Open Source Password Manager

Bitwarden, the open source password manager, makes it easy to generate and store unique passwords for any browser or device. Create your free account on the platform with end-to-end encryption and flexible integration options for you or your business.

I use Bitwarden as my main password vault. It stores my card details for automating the filling out of payment forms. Saves me from having to find or remember my card details. I also use Bitwarden for storing all of my passwords. 

Having Bitwarden as a public endpoint means that I can connect to my password vault using the Bitwarden app on Android, specifying my self hosted instance.

## Setting up the Bitwarden Server

This section of the tutorial is to set up the main Bitwarden 'hub'. This will be a publicly exposed Bitwarden API that will live on your server. 

### Step 1: Setting up your Linux server

You'll need to either have an existing server instance or create one. I use a Proxmox instance running on a server in my loft. You could also use something like [Digital Ocean](https://www.digitalocean.com/) to host your Bitwarden Server. Using the following link will give you $100 worth of credits for 60 days to play around with, just sign up using [this link](https://m.do.co/c/d2a3afe52625).

You could also use a cheap [Raspberry PI](https://amzn.to/3cWTlno) to set up your own Linux server.

Once you have the server set up, or have logged in. You'll need to do some updates and run some prerequisite installs.

    sudo apt-get update
    sudo apt-get upgrade

Next, we need to install Docker. Docker is the layer which your containers run. 

To install Docker on your instance, you need to run the following command.

The following script is a convenience script [provided by the Docker team](https://docs.docker.com/engine/install/debian/#install-using-the-convenience-script). It's highly recommended to always check what you're going to execute, before executing it.

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

### Step 2: Provisioning your Bitwarden Server

Next, you'll need to create a new folder, this will house your Bitwarden Server, you can call it anything memorable. I'll just call mine `bitwarden`

    cd ~
    mkdir bitwarden
    cd bitwarden

Next, you'll need to create a `docker-compose.yml` file. This is an orchistration file which `docker-compose` will use to provision your Docker instance.

    touch docker-compose.yml

Next, you'll need to edit your `docker-compose.yml` file and paste in the following content.

    # docker-compose.yml
    version: '3'
    
    services:
      bitwarden:
        image: bitwardenrs/server
        restart: always
        ports:
          - 8000:80
        volumes:
          - ./bw-data:/data
        environment:
          WEBSOCKET_ENABLED: 'true' # Required to use websockets
          SIGNUPS_ALLOWED: 'true'   # set to false to disable signups

I'm using [bitwarden_rs](https://github.com/dani-garcia/bitwarden_rs) as it's written in Rust, faster and more reliable. Also entirely opensource with a heavy user-base.

Save your `docker-compose.yml` file and exit back to your `bitwarden` directory.

### Step 3: Running your Bitwarden Server locally

Now, you have everything provisioned for running your Bitwarden Server.

The next thing to do is run it.

    sudo docker-compose up -d

This will start up your Bitwarden Server inside Docker, it may take some time to pull down the images.

You can eventually see your instance running by executing the following

    sudo docker ps

This will list your running instance.

If all is well, you can locally view your Bitwarden Server by navigating to `http://localhost:PORT`. Or from another machine by using your ip address instead of `localhost`

You should see something that looks like the following.
![](https://theselfhostingblog.com/content/images/2021/02/1.jpg)
Finally, you'll just need to register for an account on your new hosted instance.

Click the `Create Account` button

Then fill out your details. If you have an existing Bitwarden account, you'll still have to create a new account on this instance. You can then Export and Import between accounts.

The last thing to do is hit `Submit`
![](https://theselfhostingblog.com/content/images/2021/02/2.jpg)
If your instance isn't on your local machine, you will need to set up Nginx routing, which you can follow in Step 4.

### Step 4: Exposing your new server publicly

This part may sound scary, but it is required to allow your Bitwarden Clients (Android, iOS, Chrome extension etc) to connect to your server.

We're going to be using nginx.

#### Setting up nginx

[Nginx](https://www.nginx.com/) is a reverse proxy that allows you to point incoming web traffic to your new Bitwardeb server. 

Firstly, install nginx if you haven't already

    sudo apt-get install nginx

If you have UFW installed, you will have to Allow Nginx through your local firewall.

I have a tutorial for [setting up UFW here](https://theselfhostingblog.com/posts/setting-up-ufw-on-ubuntu-server/)

Setting Up UFW on Ubuntu Server

UFW is a program that allows you to internally control ports on your Linux instance. This gives you the ability to forward ports from your machine.
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

You can enable this by typing:

    sudo ufw allow 'Nginx Full'

Next thing to do is just double check your nginx server is up and running

    sudo systemctl status nginx

You should see something that looks like the following

    ● nginx.service - A high performance web server and a reverse proxy server
       Loaded: loaded (/lib/systemd/system/nginx.service; enabled; vendor preset: enabled)
       Active: active (running)
    ...

The next part allows us to take incoming traffic and point it to your container instance. Allowing you to expose your Bitwarden  server to the internet.

Navigate to `/etc/nginx/`

    cd /etc/nginx/
    

Use your favorite text editor and open the following file with sudo

    sudo vim nginx.conf
    

I use the following code for my syncing server

    server {
        listen 80;
        server_name vault.bowlerdesign.tech;
    
        location / {
            proxy_pass http://127.0.0.1:8000; # bitwarden server address
        }
    }
    

#### Port-forwarding

You will need to port forward your instance to allow public access to your instance. This will involve googling how to port forward from your router.

You'll need to [point port 80 and 443 to your instance](https://portforward.com/) where Nginx is set up.

#### Linking Bitwarden Server with your public domain

You will also need to set up a public domain name. This can then be used to call your new public instance with port 443 exposed.

For example, I would set up a subdomain on `bowlerdesign.tech` to be `vault.bowlerdesign.tech`. Notice this is also the domain I specified in my Nginx config above.

Here's something to search for with regards to [setting up a domain name](https://www.google.com/search?client=firefox-b-d&amp;q=point+domain+name+to+server)

#### Setting up Certbot

Certbot allows us to generate SSL certificates for free with Let's Encrypt. It's simple to install and use. Even hooks in with Nginx, meaning that there's no more manual configuration required.

To install Certbot, simply run the following command

    sudo apt-get install certbot

Then, to set up your SSL certificate, run

    sudo certbot

Follow the instructions, select your domain name from the nginx list.
Also, select `redirect` as this will upgrade any http requests to https.

### Step 5: Connecting to your new Bitwarden instance from a client.

I'm going to use the Firefox Bitwarden Plugin for this part of the tutorial. But the process is identical for all Bitwarden clients.

First, if you haven't already, install your chosen Bitwarden client and open it.

In the top left corner, click the cog icon
![](https://theselfhostingblog.com/content/images/2021/02/3.jpg)
You'll then get some configuration. Simply add your full url into the `Server URL` field
![](https://theselfhostingblog.com/content/images/2021/02/4.jpg)
Like so, then just hit `Save` and log in as normal
![](https://theselfhostingblog.com/content/images/2021/02/5.jpg)
### That's it

Pretty easy right? 

Please don't hesitate to get in touch in the comments if you get stuck. I'd be more than happy to help out with any issues you may face.
This post contains affiliate links meaning we  may receive a small commission on purchases made through links in this post. At no extra cost to you 😊
