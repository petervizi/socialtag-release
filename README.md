# socialtag-release
Debian repository of the SocialTag application

## aptly howto

```sh
aptly repo add socialtag-release debs
aptly snapshot create socialtag-2.0 from repo socialtag-release
# aptly publish snapshot -config=./aptly.conf socialtag-2.0 s3:repo.socialtag.tv:beta/

aptly -config=./aptly.conf publish switch vankman s3:repo.socialtag.tv:beta/ socialtag-2.0
```
