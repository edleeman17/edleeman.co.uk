---
title: Archiving ProtonMail Emails on a headless Ubuntu instance
slug: archiving-protonmail-emails-on-a-headless-ubuntu-instance
date: 2020-11-16T11:17:00.000Z
type: post
---



## Introduction

I wanted to be able to store all of my [ProtonMail](https://protonmail.com/) emails locally for archival purposes, with the intention of running a local content search whenever I needed something retrieving.

I'm going to talk through my steps. There's plenty of tutorials out there for email services such as; Gmail, Hotmail etc. But not much around ProtonMail, especially using a headless instance.

## ProtonMail bridge

[ProtonMail Bridge](https://protonmail.com/bridge/) is an open-source piece of software built by the Proton Team to create a dummy IMAP server locally, with a sole purpose of decrypting your emails locally to enable you to use a desktop email client such as [ThunderBird](https://www.thunderbird.net/en-US/). 

ProtonMail Bridge is a paid feature though, with a minimum requirement of the [ProtonMail Plus](https://protonmail.com/pricing) plan ($5/month). ProtonMail Bridge is not available on the ProtonMail Free plan.

## Overview

We're going to set up  a Cron job on a headless Ubuntu instance to periodically pull down all our emails. This instance will be running ProtonMail Bridge and a tool named [Offlineimap](http://www.offlineimap.org/), which will be used to store all your emails in a plaintext, searchable format. 

## Getting Started

### Step 1: Setting up your Linux server

You'll need to either have an existing server instance or create one. I use a Proxmox instance running on a server in my loft. You could also use something like [Digital Ocean](https://www.digitalocean.com/) to run your local archive. Using the following link will give you $100 worth of credits for 60 days to play around with, just sign up using [this link](https://m.do.co/c/d2a3afe52625).

You could also use a cheap [Raspberry PI](https://amzn.to/3cWTlno) to set up your own Linux server.

Once you have the server set up, or have logged in. You'll need to do some updates and run some prerequisite installs.

    sudo apt-get update
    sudo apt-get upgrade

### Step 1: gpg and pass

To use ProtonMail Bridge, you need to first set up the dependencies. These dependencies are `pass` (A password management system), which has a dependency of `gpg` (A key management system).

#### Installing GPG

GPG should be installed on your system as part of the `update and upgrade` commands that you initially ran after provisioning your server. If it's not, you can install GPG by running the following command.

    sudo apt-get install gpg

Once GPG is installed, you need to generate a GPG key.

    gpg --gen-key

This will run you through a wizard of adding your full name and email address. Also requiring you to create a passphrase for your gpg key. Add a password to satisfy the wizard, but we'll have to remove this later.

Unfortunately, ProtonMail Bridge will not work with a password protected GPG key in headless mode. This is a serious security risk, so make up your own opinion on this, do some research on what implications this has.

Once GPG has finished, you'll have a public key output. It'll look something like the following

    7BDD29402175BC627671356BE8AC4A1C3C5J6357

We now need to remove the passphrase associated with this key.

Run the following

    gpg --edit-key 7BDD29402175BC627671356BE8AC4A1C3C5J6357

Once you have executed that command, you'll be in the context of gpg

Run then next command

    passwd

You'll now need to enter the passphrase you created earlier, which will unlock the GPG key.

There will now be another console prompt to enter a new passphrase.

Leave this blank.

You'll be asked to confirm that you want a blank passphrase, it'll warn you about the security implications.

Hit 'Y' or Yes to confirm this implication.

Finally, quit the GPG context by typing `q` and hitting Enter.

#### Installing Pass

Now it's time to install Pass, which is a ProtonMail Bridge dependency.

    sudo apt-get install pass

We'll then need to initialise a new `pass` instance with your previously generated gpg key id.

    pass init 7BDD29402175BC627671356BE8AC4A1C3C5J6357

That's, all the setup required for initialising `pass`.

### Step 2: Installing ProtonMail Bridge

Now it's time to install ProtonMail Bridge.

Run the following command to install the latest version of ProtonMail Bridge at time of writing this post.

    wget https://protonmail.com/download/beta/protonmail-bridge_1.5.0-1_amd64.deb

Then install

    dpkg -i protonmail-bridge_1.5.0-1_amd64.deb

There may be some more missing dependencies when installing. To fix this, run the following

    sudo apt --fix-broken install

### Step 3: Initialising ProtonMail Bridge

We now need to log in to ProtonMail Bridge, to do this, run the following command

    protonmail-bridge --cli

ProtonMail Bridge will start up and ask you to log in with an email and a password.

This will be your standard ProtonMail username and password.

### Step 4: Getting your ProtonMail IMAP Username and Password

Whilst in the context of the ProtonMail Bridge session, run the following command.

    info

You'll see an output like the following.

                Welcome to ProtonMail Bridge interactive shell
                                  ___....___
        ^^                __..-:'':__:..:__:'':-..__
                      _.-:__:.-:'':  :  :  :'':-.:__:-._
                    .':.-:  :  :  :  :  :  :  :  :  :._:'.
                 _ :.':  :  :  :  :  :  :  :  :  :  :  :'.: _
                [ ]:  :  :  :  :  :  :  :  :  :  :  :  :  :[ ]
                [ ]:  :  :  :  :  :  :  :  :  :  :  :  :  :[ ]
       :::::::::[ ]:__:__:__:__:__:__:__:__:__:__:__:__:__:[ ]:::::::::::
       !!!!!!!!![ ]!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!![ ]!!!!!!!!!!!
       ^^^^^^^^^[ ]^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^[ ]^^^^^^^^^^^
                [ ]                                        [ ]
                [ ]                                        [ ]
          jgs   [ ]                                        [ ]
        ~~^_~^~/   \~^-~^~ _~^-~_^~-^~_^~~-^~_~^~-~_~-^~_^/   \~^ ~~_ ^
    >>> info
    Configuration for {your email}
    IMAP Settings
    Address:   127.0.0.1
    IMAP port: 1143
    Username:  {your email}
    Password:  {your password}
    Security:  STARTTLS
    
    SMTP Settings
    Address:   127.0.0.1
    IMAP port: 1025
    Username:  {your email}
    Password:  {your password}
    Security:  STARTTLS

Take a note of the values `{your email}` and `{your password}`. You'll need these later.

### Step 5: Setting up Offlineimap

I'm going to be using an open-source tool I found on Github. Written by `[peterrus](https://github.com/peterrus/protonmail-export-linux)`.

Run the following command to pull down the repo from Github.

    git clone https://github.com/peterrus/protonmail-export-linux.git

The `cd` into the cloned repo

    cd protonmail-export-linux

Next, you need to install `offlineimap`

    sudo apt-get install offlineimap

Once installed, in the `protonmail-export-linux` directory, there will be a `offlineimaprc` file. Open this with your favorite text editor. I'll be using `vim` in this example.

    vim offlineimparc

You'll see a file open that looks something like the following

    # Feel free to modify this file to your needs
    # See https://github.com/OfflineIMAP/offlineimap/blob/master/offlineimap.conf for a full reference
    
    [general]
    accounts = Protonmail
    metadata = ./offlineimap-metadata
    
    [Account Protonmail]
    localrepository = ProtonmailLocal
    remoterepository = ProtonmailRemote
    
    # Feel free to change this, or disable it by commenting it out
    postsynchook = notify-send 'Protonmail export done'
    
    [Repository ProtonmailLocal]
    type = Maildir
    localfolders = ./protonmail-export
    # If you (accidentally) delete mail locally, it won't get synced to Protonmail
    sync_deletes = no
    
    [Repository ProtonmailRemote]
    type = IMAP
    # Change this to the value provided in the Protonmail bridge
    remoteuser = {your email}
    remotepass = {your password}
    remotehost = localhost
    remoteport = 1143
    ssl = no
    starttls = no
    # If you delete mail on Protonmail, this deletion also get's synced to the archive
    expunge = yes
    # Don't try to sync local changes to Protonmail, we just want a backup
    readonly = True

Leave everything how it is, apart from the section where I have specified, `{your email}` and `{your password}`. These will need to be replaced with your ProtonMail Bridge email and password that I got you to take note of earlier.

Save your changes and exit your text editor.

### Step 6: Setting up screen

I use screen to run services in the background. Both `protonmail-bridge` and `offlineimap` need to run simultaneously.

    sudo apt-get install screen

### Step 7: Creating a startup script

I made it easy for myself and created a startup script to execute both `protonmail-bridge` and `offlineimap`

Here's my script, simply create a new file named `start-sync.sh` in your home directory. Giving it execute permissions by running

    sudo chmod +x start-sync.sh

The `start-sync.sh` file contents should look like this. 

    #! /bin/bash
    echo "killing existing screen sessions"
    pkill screen
    echo "Starting bridge"
    screen -d -m protonmail-bridge --cli
    echo "Starting sync"
    sleep 10
    screen -d -m offlineimap -c /home/{your user}/protonmail-export-linux/offlineimaprc

Change the location of your `offlineimaprc` file in that shell script.

### Step 8: Starting Offlineimap

Now it's time to execute your `start-sync.sh`

    ./start-sync.sh

Now, both of your services should have started up. To see them, run the following command

    screen -r

You'll see an output like the following

    ed@mail:~# screen -r
    There are several suitable screens on:
            6415..mail      (12/05/20 18:06:26)     (Detached)
            6308..mail      (12/05/20 18:06:16)     (Detached)
    Type "screen [-d] -r [pid.]tty.host" to resume one of them.
    ed@mail:~#

Then run

    screen -r 6415 // 6415 being the id of the top process on the screen -r output

You should see an output of a successful authentication with ProtonMail Bridge, and a list of emails currently being downloaded.

    Copy message UID 2081 (23/3445) ProtonmailRemote:All Mail -> ProtonmailLocal
    Folder INBOX [acc: Protonmail]:
    etc...

Detach from this screen by hitting `Ctrl + a` and `Ctrl + d`.

### Step 9: Where are my emails?

Whilst your emails are downloading, they will be saved to `~/protonmail-export`. You should see a list of your email folders in this directory, under the `cur` subdirectory.

### Step 10: Setting up a cron job to pull new emails

Now it's time to set this job up to run each day, or each hour, whatever you'd like to pick.

Run the following

    sudo crontab -e

At the very bottom of your `crontab` file, paste in the following command.

    0 0 * * * /home/{your user}/start-sync.sh

I use a tool called [crontab.guru](https://crontab.guru/) to assist with picking a schedule to run my command.

My command will run at midnight each day.

---

### That's all

And hopefully, everything should be up and running successfully. Let me know if you receive any issues in the comments, I'll be happy to help you out.

You could now sync all your emails to Dropbox, or something like Syncthing, which [I have recently written about here](https://theselfhostingblog.com/posts/how-to-set-up-a-headless-syncthing-network/).
This post contains affiliate links, meaning we  may receive a small commission on purchases made through links in this post. At no extra cost to you 😊 

We hate Ads! They don't respect your privacy. 

Would you consider supporting us on [buy me a coffee](https://www.buymeacoffee.com/selfhostingblog)? Your support really helps to keep the costs down with running the blog
