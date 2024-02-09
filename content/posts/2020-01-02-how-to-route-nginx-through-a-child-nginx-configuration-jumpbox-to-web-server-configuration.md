---
title: How to Route Nginx Through a Child Nginx Configuration - Jumpbox to Web Server Configuration
slug: how-to-route-nginx-through-a-child-nginx-configuration-jumpbox-to-web-server-configuration
date: 2020-01-02T11:34:00.000Z
type: "post"
---



I had a specific use case where I needed to run a docker instance, which had it's own configured nginx instance.

The issue was that I already use nginx on my JumpBox.

The fix was relatively self explanatory, but I wanted somewhere to write down the issues that I had to tackle.

## The Solution

So the solution is just to point nginx (JumpBox) to the other nginx instance (docker).

> Just to let you know, in my case, there are separate physical servers. The configuration will not differ, but you may need to internally expose ports between hosts if you have something like UFW installed. [I have a tutorial here on how to set up UFW.](https://blog.bowlerdesign.tech/2019/12/15/setting-up-ufw-on-ubuntu-server/)

So on my Host `B` I have a web instance running on port `8080`. This web instance is an nginx reverse proxy that is pointing to another docker instance within the same docker network on the machine.

Host `A` is my existing nginx reverse proxy.

The quick solution is to forward your call from Host `A` to Host `B`.

Like so

    server {
      server_name blog.bowlerdesign.tech;
    
      location / {
        proxy_pass http://host_running_blog:8080;
      }
    

I ran into issues here, I couldn't get css loading properly when navigating to blog.bowlerdesign.tech.

I was missing headers in the request. Here's an ideal configuration for setting up a website.

    server {
      server_name blog.bowlerdesign.tech;
    
      location / {
        proxy_pass http://host_running_blog:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto scheme;
        proxy_pass_header Content-Type;
      }
    
    

This will forward the necessary headers for your host.
