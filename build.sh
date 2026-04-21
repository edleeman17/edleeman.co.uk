#!/bin/sh
set -e
hugo
npx --yes pagefind --site public
