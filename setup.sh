#!/usr/bin/env sh

set -ex

KEY_ID=6C72CD1959DF7DEC
gpg --recv ${KEY_ID}
gpg --armor --export ${KEY_ID} | sudo apt-key add

echo "deb https://s3-us-west-1.amazonaws.com/repo.socialtag.tv/beta/ vankman main" > /etc/apt/sources.list.d/socialtag.list
apt-get -y update
apt-get -y install socialtag-raspberry-system

THE_NEW_HOSTNAME=$(cat /sys/class/net/eth0/address | tr -d ':')
echo ${THE_NEW_HOSTNAME} > /etc/hostname
echo "127.0.0.1 ${THE_NEW_HOSTNAME}" >> /etc/hosts
