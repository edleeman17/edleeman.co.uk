---
title: "Assuming an AWS Role in CI/CD"
date: 2024-02-09T13:30:38Z
draft: false
type: "note"
tags:
    - knowledge
---
# Assuming an AWS Role in CI/CD 

```bash
ROLE_UUID=$(uuidgen)
TMPFILE=$(mktemp) || exit 1
export aws_region=${AWS_REGION}

aws sts assume-role --role-arn arn:aws:iam::0123456789:role/publisher-role --role-session-name role_$ROLE_UUID > $TMPFILE

if [ ! -s $TMPFILE ]; then
    echo "!!! AWS Credentials file empty !!!"
    exit 1
fi

export AWS_ACCESS_KEY_ID=$(cat $TMPFILE | jq -r ."Credentials"."AccessKeyId")
export AWS_SECRET_ACCESS_KEY=$(cat $TMPFILE | jq -r ."Credentials"."SecretAccessKey")
export AWS_SESSION_TOKEN=$(cat $TMPFILE | jq -r ."Credentials"."SessionToken")
export AWS_DEFAULT_REGION=$aws_region
```

Assume role doesn’t export the new AWS credentials, so we need to export the new variable values ourselves
