#!/usr/bin/env python3
import argparse
import base64

def base64_encode_file(file_name):
    with open(file_name) as file_handler:
        patch = file_handler.read()
        return base64.b64encode(patch.encode('ascii')).decode('ascii')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('setup_file')
    parser.add_argument('wpa_supplicant_patch')
    parser.add_argument('config_txt_patch')

    args = parser.parse_args()

    wpa_supplicant_patch_str = base64_encode_file(args.wpa_supplicant_patch)
    config_txt_patch_str = base64_encode_file(args.config_txt_patch)

    SETUP_SH = f'''#!/usr/bin/env sh

set -ex

# from https://keys.openpgp.org/
KEY_ID=730878BE36688D52
gpg --keyserver https://keys.openpgp.org:443 --recv ${{KEY_ID}}
gpg --armor --export ${{KEY_ID}} | apt-key add

echo "deb https://s3-us-west-1.amazonaws.com/repo.socialtag.tv/beta/ vankman main" > /etc/apt/sources.list.d/socialtag.list
apt-get -y update
apt-get -y install socialtag-raspberry-system

THE_NEW_HOSTNAME=$(cat /sys/class/net/eth0/address | tr -d ':')
echo ${{THE_NEW_HOSTNAME}} > /etc/hostname
echo "127.0.0.1 ${{THE_NEW_HOSTNAME}}" >> /etc/hosts

systemctl disable wpa_supplicant.service

echo "{wpa_supplicant_patch_str}" | base64 --decode > 10-wpa_supplicant.patch

patch /lib/dhcpcd/dhcpcd-hooks/10-wpa_supplicant 10-wpa_supplicant.patch

echo "{config_txt_patch_str}" | base64 --decode > config.txt.patch

patch /boot/config.txt config.txt.patch
'''

    with open(args.setup_file, 'w') as setup_file:
        setup_file.write(SETUP_SH)
