#!/bin/sh
# This deploy script can be executed from the Git post-receive hook.
# We assume that the application is installed in $HOME/$APPNAME.
export HOME="/home/{{ server_user }}"
APPNAME="{{ project_name }}"
APPHOME="$HOME/$APPNAME"
cd "$APPHOME"
echo "--------------------------------"
echo "Deploying $APPNAME"
echo "--------------------------------"
/usr/bin/git pull
# Install any new pip packages
"$HOME/.virtualenvs/$APPNAME/bin/pip" install -r requirements.txt
cd "$APPHOME/$APPNAME"
# Generate static files
"$HOME/.virtualenvs/$APPNAME/bin/python" manage.py collectstatic -v 0 --link --noinput
"$HOME/.virtualenvs/$APPNAME/bin/python" manage.py generatemedia
# Restart Upstart server
sudo stop $APPNAME
sudo start $APPNAME
