---
title: "Installing Commands Using Existing Docker Images"
date: 2024-02-09T13:28:26Z
draft: false
type: "note"
---
# Installing commands using existing Docker Images

```dockerfile
COPY --from=library/docker:latest /usr/local/bin/docker /usr/bin/docker
COPY --from=docker/compose:latest /usr/local/bin/docker-compose /usr/bin/docker-compose
```
