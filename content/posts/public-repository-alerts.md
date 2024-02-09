---
title: "Dabbling with Bash, public repository alerting"
date: 2021-03-25T14:04:59Z
draft: false
type: "post"
---

I have been playing around with Bash over the last 24 hours, which has had its highs and lows.

I still don't understand when to echo a variable into another variable and when to do a direct assignment. But it's early days for me. I'm looking to take a more architectural approach to my day job, which means spending even more time in the Linux environment. I'd like to automate a lot of my repetitive tasks, reason 1 being that I save some time, reason 2 being that I will definitely forget to do the task.

My first task that I wanted to automate was to make sure that the company I work for, only creates private repositories. I have written a script below which calls the GitHub API and sends an alert email to a designated email address if a public repository is created. Not exactly rocket science, but fits a purpose for me. 

I figured I'd share it, I haven't Google'd to see whether it already exists though...

``` bash
#!/bin/bash -l


# This will call the GitHub API
# checking to see whether any internal repositories
# have been made public by accident. Then alerting
# via an email.

# Required Params:
# GITHUB_ORG (Name of the GitHub Organisation)
# EMAIL_TO (Where to send the email notification)
# EMAIL_FROM (Where to send the email from)

PUBLIC_REPO_KEY=$(curl -s https://api.github.com/orgs/$GITHUB_ORG | grep -P '"public_repos":.*?\d');

PUBLIC_REPO_COUNT=$(echo $PUBLIC_REPO_KEY | grep -o -E '[0-9]+');

if [ $PUBLIC_REPO_COUNT -gt 0 ]
then
    PUBLIC_REPO_LIST=$(curl -s https://api.github.com/orgs/$GITHUB_ORG/repos?type=public\&per_page=100 | grep -P 'full_name');
    PUBLIC_REPO_LIST_NAMES=`echo $PUBLIC_REPO_LIST | grep -o "$GITHUB_ORG[^\"]*"`;

    echo "To: ${EMAIL_TO}"                                                  | tee -a "email.txt";
    echo "Subject: [IMPORTANT]: Public Repository exposed in ${GITHUB_ORG}" | tee -a "email.txt";

    echo `date`                                                             | tee -a "public-repo.log" "email.txt";
    echo The following repositories are PUBLIC                              | tee -a "public-repo.log" "email.txt";
    echo --------------------------------------                             | tee -a "public-repo.log" "email.txt";
    echo $PUBLIC_REPO_LIST_NAMES | tr " " "\n"                              | tee -a "public-repo.log" "email.txt";
    echo --------------------------------------                             | tee -a "public-repo.log" "email.txt";

    # Send via email.
    sendmail -t -f $EMAIL_FROM < email.txt;

    # clear temporary email file
    > email.txt;
fi
```

As you might be able to work out, it calls the GitHub API, 'greps' out the number of public repos and sends an email with a list of those public repos to a defined email address. You can define the environment variables in your `~/.bashrc`. The first line does something magic with `#!/bin/bash -l`, something about the `-l` means that a cronjob will load in the environment variables from your `~/.bashrc`. I haven't looked into how this works yet, but it's pretty damn cool.

Anyway, a little bit about my dev side.
