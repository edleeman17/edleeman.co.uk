---
title: "Day 10 - Deleted docker-compose"
date: 2021-03-26T21:49:09Z
draft: false
---

Today, we ran out of space on a drive which was running an internal wiki. Unfortunately for us, we lost the docker-compose file which contained the database password used to get the data for our wiki.

Luckily, the container was still running, even if it wasn't we probably could have spun up an old containers using something from `docker ps -a`.

As the container was still running, we exec'd into it with `docker exec -it <container_id> bash` and we're able to run the `env` command which revealed the password that was set in the docker-compose file. 

Therefore, we we're able to reconstruct the docker-compose file and restart the wiki.
