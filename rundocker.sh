#!/usr/bin/env bash

docker stop discord_bot
docker rm discord_bot
# shellcheck disable=SC2046
docker run -it -d --restart=always --name=discord_bot $(docker build -q .)