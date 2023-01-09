---
title: Setting Up UFW on Ubuntu Server
slug: setting-up-ufw-on-ubuntu-server
date: 2019-12-15T11:29:00.000Z
type: post
---



[UFW](https://help.ubuntu.com/community/UFW) (Uncomplicated Firewall) is a program that allows you to internally control ports on your Linux instance. This gives you the ability to forward ports from your machine.

The common use of a firewall is to control the ports that have access from the outside world, for instance, running a website would need ports `80`/`443` exposed on your network to be able to route your site.

UFW is different, think of port forwarding, but between local instances. You can lock down internal exposure to port `22` (`ssh`) for example.

## Why? What's the point?

Security.

In the coming weeks, I'll be writing blog posts on how I have set up my jumpbox server. UFW plays a key part in my setup. I have used UFW to only open port 22 on my jumpbox server. I can `ssh` in, but that's it. No other ports can be attacked or sniffed.

From the jumpbox server I can then **only**`ssh` into my other internal instances. This means that if I wanted to `ssh` into server `B` I would have to go via the jumpbox `A`.

## I think I get it, how can I install it?

We're running [Ubuntu Server on a Raspberry Pi](https://ubuntu.com/download/raspberry-pi). But these instructions are for all Debian instances, the Raspberry Pi is irrelevant for this tutorial.

### Let's install

1. Install UFW

`sudo apt-get install ufw`

1. Check the status of UFW

`sudo ufw status`

You should see that UFW is **disabled**

1. Let's allow some ports, it's really important that you allow your `ssh` port, otherwise you can lose access when we get round to enabling UFW.

The default `ssh` port is **22** unless you have changed the default port.

`sudo ufw allow 22`

You can use the above command to allow the necessary ports for your instance. We're just going to stick with port `22` for this example.

1. Let's enable UFW

`sudo ufw enable`

## That's it

You now have a firewall running on your local instance, locked down to be only accessible by port `22`.

In the future, if you're running services on this box, you'll need to expose any other ports that you want to have access outside of your machine. Let's say you set up [OpenVPN](https://openvpn.net/), you have to expose port `1194` on the machine it's running on.

## Thanks for reading

Thanks for reading, hope I've helped in some way!
