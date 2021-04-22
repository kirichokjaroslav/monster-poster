## Posterify

**: About :**

A tiny microservice congratulating employees on the anniversary of their work in the company. What is he doing? It takes a previously uploaded employee's photo, combines it with a «congratulating template» and when the day **«x»** comes, - sends the resulting poster to the general channel the **«slack»** messenger.

**: How to use :**

There are several ways to start the service:
- Manual: way - I

 1. After repository cloning, go to the service directory. Using any tool for managing a virtual environment, create it:

            virtualenv --python = python3.7 .pyenv

 2. As soon as it is created, activate:

            source .pyenv/bin/activate

 3. Next, install the libraries and dependencies:

            pip install -r requirements.txt --no-cache-dir

 4. And launch:

            python launch.py -r [--release], or -h


- Manual: way - II

 1. For greater convenience, made an automatic installation and configuration file. Just need to launch:

            ./bootstrap.dev.sh or ./bootstrap.production.sh

 2. Follow installer questions and recommendations

 3. After all launch:

            python launch.py -r [--release], or -h
