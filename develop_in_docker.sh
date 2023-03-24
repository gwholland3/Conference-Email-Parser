#!/bin/sh
touch .bash_history \
&& docker run --rm -it \
    --hostname conf-email-dev \
    --name conf-email-dev \
    -v "$PWD/src:/usr/app/src" \
    -v "$PWD/data:/usr/app/data" \
    -v "$PWD/docs:/usr/app/docs" \
    -v "$PWD/.bash_history:/root/.bash_history" \
    $(docker build -q .) \
    bash
