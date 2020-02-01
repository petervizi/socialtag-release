#!/usr/bin/env sh

set -ex

KEY_ID=6C72CD1959DF7DEC
gpg --recv ${KEY_ID}
gpg --armor --export ${KEY_ID} | sudo apt-key add

echo "deb https://s3-us-west-1.amazonaws.com/repo.socialtag.tv/beta/ vankman main" | sudo tee -a /etc/apt/sources.list.d/socialtag.list
