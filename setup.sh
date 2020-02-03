#!/usr/bin/env sh

set -ex

KEY_ID=6C72CD1959DF7DEC
gpg --recv ${KEY_ID}
gpg --armor --export ${KEY_ID} | apt-key add

echo "deb https://s3-us-west-1.amazonaws.com/repo.socialtag.tv/beta/ vankman main" > /etc/apt/sources.list.d/socialtag.list
apt-get -y update
apt-get -y install socialtag-raspberry-system

THE_NEW_HOSTNAME=$(cat /sys/class/net/eth0/address | tr -d ':')
echo ${THE_NEW_HOSTNAME} > /etc/hostname
echo "127.0.0.1 ${THE_NEW_HOSTNAME}" >> /etc/hosts

systemctl disable wpa_supplicant.service

echo "LS0tIDEwLXdwYV9zdXBwbGljYW50CTIwMTktMTItMDkgMDU6MjY6MjkuOTQzNDA3Njg3IC0xMDAw
CisrKyAvbGliL2RoY3BjZC9kaGNwY2QtaG9va3MvMTAtd3BhX3N1cHBsaWNhbnQJMjAxOS0xMS0z
MCAwNjoyMToxMS4zNjAzODIzMzggLTEwMDAKQEAgLTU5LDcgKzU5LDcgQEAKIAlzeXNsb2cgaW5m
byAic3RhcnRpbmcgd3BhX3N1cHBsaWNhbnQiCiAJd3BhX3N1cHBsaWNhbnRfZHJpdmVyPSIke3dw
YV9zdXBwbGljYW50X2RyaXZlcjotbmw4MDIxMSx3ZXh0fSIKIAlkcml2ZXI9JHt3cGFfc3VwcGxp
Y2FudF9kcml2ZXI6Ky1EfSR3cGFfc3VwcGxpY2FudF9kcml2ZXIKLQllcnI9JCh3cGFfc3VwcGxp
Y2FudCAtQiAtYyIkd3BhX3N1cHBsaWNhbnRfY29uZiIgLWkiJGludGVyZmFjZSIgXAorCWVycj0k
KHdwYV9zdXBwbGljYW50IC11IC1CIC1jIiR3cGFfc3VwcGxpY2FudF9jb25mIiAtaSIkaW50ZXJm
YWNlIiBcCiAJICAgICIkZHJpdmVyIiAyPiYxKQogCWVycm49JD8KIAlpZiBbICRlcnJuICE9IDAg
XTsgdGhlbgo=" | base64 --decode > 10-wpa_supplicant.patch

patch < 10-wpa_supplicant.patch
