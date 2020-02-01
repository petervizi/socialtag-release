# socialtag-release
Debian repository of the SocialTag application

## get setup.sh

```sh
curl -sL -osetup.sh https://bit.ly/2S8GZN0
```

## aptly howto

```sh
aptly repo add socialtag-release debs
aptly snapshot create socialtag-2.0 from repo socialtag-release
# aptly publish snapshot -config=./aptly.conf socialtag-2.0 s3:repo.socialtag.tv:beta/

aptly -config=./aptly.conf publish switch vankman s3:repo.socialtag.tv:beta/ socialtag-2.0
```
