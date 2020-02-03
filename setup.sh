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

cat <<EOF > 10-wpa_supplicant.patch
--- 10-wpa_supplicant	2019-12-09 05:26:29.943407687 -1000
+++ /lib/dhcpcd/dhcpcd-hooks/10-wpa_supplicant	2019-11-30 06:21:11.360382338 -1000
@@ -59,7 +59,7 @@
 	syslog info "starting wpa_supplicant"
 	wpa_supplicant_driver="${wpa_supplicant_driver:-nl80211,wext}"
 	driver=${wpa_supplicant_driver:+-D}$wpa_supplicant_driver
-	err=$(wpa_supplicant -B -c"$wpa_supplicant_conf" -i"$interface" \
+	err=$(wpa_supplicant -u -B -c"$wpa_supplicant_conf" -i"$interface" \
 	    "$driver" 2>&1)
 	errn=$?
 	if [ $errn != 0 ]; then
  EOF

  patch < 10-wpa_supplicant.patch
