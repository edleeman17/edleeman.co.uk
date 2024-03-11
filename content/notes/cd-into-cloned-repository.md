---
title: "CD into a cloned git repository"
date: 2024-03-11T17:56:22Z
draft: false
type: "note"
image: images/apple-touch-icon.png
---

# CD into a cloned Git repository

Regularly I clone down repositories into a directory and then have to manually pluck the repository name out of the clone URL to `cd` into the cloned directory.

I found the following snippet which will extract the repository name out of the clone url and `cd` into it.

```shell
# ~/.zshrc/.bashrc/whatever...
alias cdr='cd $(basename $_ .git)'
```

This can then be used as...

```shell
~ git clone my-repository-url 
~ cdr
~/my-repository
```
Or even better...

```shell
# ~/.zshrc/.bashrc/whatever...
function git() {
    if [ $1 = "clone" ]
    then 
        command git $@ && cd "$(basename "$_" .git)"
    else
        command git $@
    fi
}
```

[source](https://stackoverflow.com/questions/59392153/git-clone-and-cd-into-it)
