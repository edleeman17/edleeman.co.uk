---
title: Self-hosting a Wireguard VPN, the easy way
slug: self-hosting-a-wireguard-vpn-the-easy-way
date: 2020-09-13T19:49:07.000Z
type: "post"
---



## Introduction

We're going to cover setting up a Wireguard VPN on your home server or cloud service. For secure remote access to your internal network, or a cheap, secure connection to a cloud service for *some* increased privacy when browsing online.
VPN's don't make you anonymous, there's a lot of stigma around this. Here's some [helpful information](https://www.privacytools.io/providers/vpn/) if you want to read into this some more.

## Setting up Wireguard, the easy way

I initially found setting up Wireguard confusing. Keys kept getting mixed up, I had no way of sending public keys between devices so that I could set up a client on my mobile device etc..

After around 30 seconds of lazy Duck Duck Go'ing (Not quite the same ring to it). I found a script on Github provided by [angristan](https://github.com/angristan). Here's [the repo](https://github.com/angristan/wireguard-install).

It's just a bash script which does all of the config for you, but still providing user prompts for entering the public server IP and choosing a preferred DNS address for the server.

### Step 1: Clone and execute the Wireguard Installer

After ssh'ing to your server, whether it's local, or cloud-hosted. If you're thinking of cloud hosting your Wireguard VPN for some privacy, I'd highly recommend using [Digital Ocean](https://www.digitalocean.com/). Using the following link will give you $100 worth of credits for 60 days to play around with, just sign up using [this link](https://m.do.co/c/d2a3afe52625).

You could also use a cheap [Raspberry PI](https://amzn.to/3cWTlno) to set up your own Linux server.

Anyway, after you have accessed your machine, we need to pull down the Wireguard installer code from Github. We're just going to `curl` it.

    curl -O https://raw.githubusercontent.com/angristan/wireguard-install/master/wireguard-install.sh

Now we just need to change the file permissions to allow execution of the new `.sh` scipt we've just downloaded.

    sudo chmod +x wireguard-install.sh

Finally, execute the Wireguard Installer

    sudo ./wireguard-install.sh

### Step 2: Configuring Wireguard

This is the easy part.

You'll see below the process of setting up Wireguard using the Wireguard Installer. All of the values below were picked for me, I just had to hit `return` a few times.

    ➜  Ed sudo ./wireguard-install.sh
    Welcome to the WireGuard installer!
    The git repository is available at: https://github.com/angristan/wireguard-install
    
    I need to ask you a few questions before starting the setup.
    You can leave the default options and just press enter if you are ok with them.
    
    IPv4 or IPv6 public address: 37.120.198.182
    Public interface: eth2
    WireGuard interface name: wg0
    Server's WireGuard IPv4: 10.66.66.1
    Server's WireGuard IPv6: fd42:42:42::1
    Server's WireGuard port [1-65535]: 57281
    First DNS resolver to use for the clients: 176.103.130.130
    Second DNS resolver to use for the clients (optional): 176.103.130.131
    
    Okay, that was all I needed. We are ready to setup your WireGuard server now.
    You will be able to generate a client at the end of the installation.
    Press any key to continue...

After running through those steps above, the Wireguard Installer will do its thing and set up Wireguard for you. You'll eventually be left with a prompt to set up a new client.

    Tell me a name for the client.
    The name must consist of alphanumeric character. It may also include an underscore or a dash.
    Client name: Phone
    Client's WireGuard IPv4: 10.66.66.2
    Client's WireGuard IPv6: fd42:42:42::2

Here's my config, I just entered a name and the rest was generated for me.

What's also really cool, is that a QR code gets generated in the console window, which you can scan with your new device.

You'll also have a `.conf` file generated for you to copy to your device.

### Portforwarding

Remember we had to specify a port? We'll need to forward that. There are a million different tutorials on the web for how to port-forward for your router. 

Here's a [handy guide.](https://portforward.com/)

### Final steps

All that's now left to do is to set up Wireguard on your device. Simply download the required app/program onto your machine and either scan the provided QR code or import that `.conf` file into your client.

Then enable your VPN. Let me know how it goes.
This post contains affiliate links meaning we  may receive a small commission on purchases made through links in this post. At no extra cost to you 😊
