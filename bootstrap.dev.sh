#!/usr/bin/env bash

# This script will install apt-get and brew dependencies as well as install autoenv
# which will automatically activate your virtual environment when you `cd` into this directory.
#
# Feel free to update this file with your own os-level dependencies :)

# See if we have either brew or apt-get installed
APT_CMD=$(which apt-get)
BREW_CMD=$(which brew)

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

elif [ ! -z $BREW_CMD ]; then
    # What to install with `brew`
    echo "${COLOR_YLW}...Installing brew dependencies...${COLOR_DEF}";
    brew install --upgrade python3.$PYTHON_MINOR_VERSION

else
    echo "${COLOR_RED}Neither brew or apt-get are installed. Exiting!${COLOR_DEF}"
    exit 1;
fi

echo "${COLOR_YLW}...Installing virtualenv...${COLOR_DEF}";
pip3 install virtualenv

echo "${COLOR_YLW}...Checking for autoenv installation...${COLOR_DEF}";
pip3 freeze | grep -q autoenv
autoenv_installed=$?
if [ ! ${autoenv_installed} -eq 0 ]; then
    read -r -p "Autoenv will automatically activate this virtualenv when you 'cd' into the directory. Do you want to install autoenv? [y/n]" response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            pip3 install autoenv

            read -p "Bash startup file [~/.bashrc]: " BASHRC
            BASHRC=${BASHRC:-~/.bashrc}
            BASHRC_ABS=`eval echo ${BASHRC//>}`

            # Check if their bash file has autoenv activated in it, if not, see if they want to add it
            if ! grep -q "activate" $BASHRC_ABS ; then
                echo "${COLOR_YLW}...Adding autoenv to $BASHRC...${COLOR_DEF}";
                echo "# activate autoenv" >> $BASHRC_ABS
                echo "source `which activate`" >> $BASHRC_ABS
                echo "cd ." >> $BASHRC_ABS
            fi
    fi
else
    echo "Autoenv already installed.";
fi

PYENV=.pyenv

# Create the actual virtualenv
if [ ! -d $PYENV ]; then
    echo "${COLOR_YLW}...Creating virtual env...${COLOR_DEF}"
    virtualenv --python=python3.$PYTHON_MINOR_VERSION $PYENV --no-site-packages
fi

# If we have a requirements file, install them reqs
if [ -f requirements.txt ]; then
    echo "${COLOR_YLW}...Installing pip requirements...${COLOR_DEF}"
    source $PYENV/bin/activate
    pip3 install -r requirements.txt --no-cache-dir
fi

echo "${COLOR_YLW}...Installation completed...${COLOR_DEF}";

if [ ! -z "${BASHRC}" ]; then
    echo "
    Please run:
        ${COLOR_YLW}source $BASHRC${COLOR_DEF}
    ";
else
    echo "
    Please run:
        ${COLOR_YLW}source $PYENV/bin/activate${COLOR_DEF}
    ";
fi
