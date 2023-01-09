---
title: Host your static blog for free with the Digital Ocean App Platform
slug: host-your-blog-for-free-with-digital-ocean-apps
date: 2021-03-15T15:57:01.000Z
type: post
---



## Digital Ocean

### What is Digital Ocean's App Platform?

[Digital Ocean](https://www.digitalocean.com/) has introduced a new product called [App Platform](https://www.digitalocean.com/products/app-platform/) which allows developers to quickly and easily build, deploy and scale apps. Digital Ocean will manage the solution for you, which means that the infrastructure, HTTPS, CDN and DNS routing is all done for you. This is awesome as it makes deploying apps simple.

With [Digital Ocean's App Platform](https://www.digitalocean.com/products/app-platform/), there is also the offer to host 3 static sites for free using their Starter pricing structure. 
![](https://theselfhostingblog.com/content/images/2021/03/image-12.png)Digital Ocean's Starter offerings
### What is a static site?

A static website is essentially images and text. Each page is fixed with the content that was written by the author. Static sites are the most basic type of website and are the easiest to create.

### Supported static site generators

Below are some examples of static site generators that [Digital Ocean supports](https://www.digitalocean.com/docs/app-platform/languages-frameworks/)

- [Hugo](https://gohugo.io/)
- [Jekyll](https://jekyllrb.com/)
- [Nuxt.js](https://nuxtjs.org/)
- [Gatsby](https://www.gatsbyjs.com/)
- [Next.js](https://nextjs.org/)

For this tutorial, we're going to be using Hugo!

## Setting up your static Hugo site

This is just going to be a brief walkthrough of how to get a Hugo site set up. I won't show you how to use Hugo. You can follow [their quickstart guide](https://gohugo.io/getting-started/quick-start/) to get familiar with Hugo

### Installing Hugo locally

To get up and running, we need to install the Hugo CLI on to our local environment. This will allow us to provision a new website, write posts and deploy it to our server. Don't panic though, this isn't where your website is going to be hosted. It's just where the tool lives to generate your website and write content

I'll be setting it up on my local Windows 10 machine with WSL installed. There are [other setup instructions](https://gohugo.io/getting-started/installing/) if you're not using WSL Windows. Such as Homebrew.

Anyway, WSL instructions.

Make sure you're fully up to date.

    sudo apt-get update
    sudo apt-get upgrade

Next, we just need to pull down Hugo.

    sudo apt-get install hugo

Once installed, we can create a new site. It doesn't matter where we create it, as we'll be committing it to Github to allow Digital Ocean to deploy our site!

    hugo new site example.com

This will create a new directory, this is your website directory. 

The Hugo output will look something like this.
![](https://theselfhostingblog.com/content/images/2021/03/image-13.png)
Awesome! all good.

Now, we need to create a Git repository to allow us to commit our website to [Github](https://github.com/).

It's worth noting that Digital Ocean also supports [GitLab](https://about.gitlab.com/), so whichever you feel most comfortable with.

Change directory into your new website directory.

    cd example.com

## Configuring source-control

### Initialising Git

Now we just need to initialise the Git repository.

    git init

If you don't have git installed, just run the following.

    sudo apt-get install git

### Creating a new repository

We now need to navigate to GitHub (or GitLab) and create a new repository. This can be private if you want it to be!
![](https://theselfhostingblog.com/content/images/2021/03/image-14.png)
Once configured, Create the repository!
![](https://theselfhostingblog.com/content/images/2021/03/image-15.png)
Now, we need to follow the steps under the `...or push an existing repository from the command line`

Back on WSL, we need to run the suggested commands to tie our local Git repository with the Github repository.

Make sure you're in the root of your website directory, where we added the `.git` file.

    cd example.com

We now need to hook our Git repository up to Github.

Configure the origin.

    git remote add origin git@github.com:edleeman17/example.com.git

Now, we need to get Hugo to generate the site for us.

    hugo -D

This will produce a `public/` directory which will contain our static site files.

We now need to add all these files to our Git branch

    git add *

Add a commit message

    git commit -m "Initial commit"

Push our changes up to the origin.

    git push -u origin master

Once pushed, you should see something like this on GitHub!
![](https://theselfhostingblog.com/content/images/2021/03/image-16.png)
## Setting up Digital Ocean

### Creating an account

You need to navigate to Digital Ocean and create a new account. Using [this link](https://m.do.co/c/d2a3afe52625) will give you $100 worth of credits for 60 days to play around with. This is perfect if you want to use Digital Ocean for spinning up [Valheim servers](https://theselfhostingblog.com/posts/setting-up-a-valheim-server-using-docker/) or [Bitwarden Instances](https://theselfhostingblog.com/posts/how-to-self-host-bitwarden-on-ubuntu-server/).

You don't need any credits to host your Hugo site.

### Setting up a new App

Once you have an account, you should [navigate to the Apps section](https://cloud.digitalocean.com/apps). And then click on Create App.
![](https://theselfhostingblog.com/content/images/2021/03/image-17.png)
So, depending on which source you used, you need to click one of the sources shown.

We used GitHub, so I'm going to click GitHub.

Next, we need to select our repository.
![](https://theselfhostingblog.com/content/images/2021/03/image-18.png)
And then the branch.
![](https://theselfhostingblog.com/content/images/2021/03/image-19.png)
Digital Ocean will then detect that Hugo is the static site in your Git repository.
![](https://theselfhostingblog.com/content/images/2021/03/image-20.png)
You can leave all these values as default. Hit Next.

Now, give your site a name. This is just for internal purposes to Digital Ocean.
![](https://theselfhostingblog.com/content/images/2021/03/image-21.png)
Finally, select the Starter package and hit Launch Starter App
![](https://theselfhostingblog.com/content/images/2021/03/image-22.png)
### Deploying your App

Once you have clicked Launch Starter App, you'll be taken to your App dashboard.
![](https://theselfhostingblog.com/content/images/2021/03/image-23.png)
You can see that Digital Ocean is now building our app and deploying it. You'll know when your site is live when you see "Deployed successfully!" at the top of your dashboard.
![](https://theselfhostingblog.com/content/images/2021/03/image-24.png)
Let's go see our website. Click on the Live App button.
![](https://theselfhostingblog.com/content/images/2021/03/image-25.png)
Sweet! we have a live URL! and an SSL certificate! Now, there's no content because we haven't configured any yet. Refer back to the Hugo quickstart guide for adding pages etc. 

Make sure to commit your changes to the Git repository and Digital Ocean will automatically poll your Git repository and deploy any new changes.

### Configuring your domain name

We can now point a nicer looking domain name at our website. You should already have a domain name in mind. But if not, you can pick up a cheap one from [NameCheap](https://www.namecheap.com/).

On your App dashboard, click on the settings tab.
![](https://theselfhostingblog.com/content/images/2021/03/image-26.png)
Down the list, you will find the Domains section. Click Edit.
![](https://theselfhostingblog.com/content/images/2021/03/image-27.png)
Then click Add Domain.
![](https://theselfhostingblog.com/content/images/2021/03/image-28.png)
Enter the domain name that you have just purchased.

You have two options here, either allow Digital Ocean to manage your DNS records and point your domain to their server. Or manually manage your domain to point to their servers.

Out of simplicity, I'm going to allow Digital Ocean to manage my domain.

You need to log into your domain name provider and change the nameservers to point to Digital Ocean.

- ns1.digitalocean.com
- ns2.digitalocean.com
- ns3.digitalocean.com

Once done, Add your domain.
![](https://theselfhostingblog.com/content/images/2021/03/image-29.png)
You'll see that the custom domain name is now pending. Now, DNS is a magical thing, it'll take 24 hours for your domain name to point to your Digital Ocean app. Just give it time, try navigating from a different machine, incognito, from 4G etc.. eventually, you will see your site pop up.

## The long wait

Wait for your DNS to propagate, after that, there's not much more to it. Simply use the Hugo tool to write your posts. Commit to GitHub. Enjoy your site.

Thanks for reading along, hopefully, it helped you out. Feel free to add any comments down below!
This post contains affiliate links, meaning we  may receive a small commission on purchases made through links in this post. At no extra cost to you 😊 

We hate Ads! They don't respect your privacy. 

Would you consider supporting us on [buy me a coffee](https://www.buymeacoffee.com/selfhostingblog)? Your support really helps to keep the costs down with running the blog
