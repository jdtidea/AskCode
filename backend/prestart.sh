#!/bin/sh

##this script will run automatically before the server scripts trigger as long as this file is present in the PRESTART path
#sed -i "s/SSH_PORT/$SSH_PORT/g" /etc/ssh/sshd_config
#service ssh start
#
## Get environment variables to show up in SSH session
#eval $(printenv | sed -n "s/^\([^=]\+\)=\(.*\)$/export \1=\2/p" | sed 's/"/\\\"/g' | sed '/=/s//="/' | sed 's/$/"/' >> /etc/profile)

echo "pre-start"