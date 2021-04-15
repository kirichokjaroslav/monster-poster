#!/usr/bin/env bash

# This script will install apt-get and brew dependencies as well as install autoenv
# which will automatically activate your virtual environment when you `cd` into this directory.
#
# Feel free to update this file with your own os-level dependencies :)

# See if we have apt-get installed
APT_CMD=$(which apt-get)

# Set minor python version
PYTHON_MINOR_VERSION=7

# Сolors for better text readability
COLOR_RED=`tput setaf 1`
COLOR_DEF=`tput sgr0`
COLOR_YLW=`tput setaf 3`

if [ ! -z $APT_CMD ]; then
    # What to install with `apt-get`
    echo "${COLOR_YLW}...Installing python3...${COLOR_DEF}";
    sudo apt-get install -y python3.$PYTHON_MINOR_VERSION python3.$PYTHON_MINOR_VERSION-dev python3-pip
else
    echo "${COLOR_RED}Command 'apt-get' not found. Exiting!${COLOR_DEF}"
    exit 1;
fi

# If we have a requirements file, install them reqs
if [ -f requirements.txt ]; then
    echo "${COLOR_YLW}...Installing pip requirements...${COLOR_DEF}"
    pip3 install -r requirements.txt --no-cache-dir
fi

echo "${COLOR_YLW}...Installation completed...${COLOR_DEF}";
