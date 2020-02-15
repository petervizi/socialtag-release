#!./python-env/bin/python3
import argparse
import docker
import os
import tarfile
import aptly_api
import re

ARCH_MAP = {
    'socialtaggallery': 'armv7l',
    'socialtag-ble-configurator': 'armhf'
}


class Release:
    def __init__(self, package_name, new_version, docker_client, aptly_client):
        self.package_name = package_name
        self.new_version = new_version
        self.docker_client = docker_client
        self.aptly_client = aptly_client

        self.aptly_repo_name = 'socialtag-release'

    def fetch(self, pull):
        docker_image_name = f'petervizi/{self.package_name}:{self.new_version}'
        if pull:
            docker_image = self.docker_client.images.pull(docker_image_name)
        else:
            docker_image = self.docker_client.images.get(docker_image_name)
        print(docker_image)
        container = self.docker_client.containers.create(docker_image)
        print(container)

        arch = ARCH_MAP[self.package_name]
        deb_file_name = f'{self.package_name}_{self.new_version}_{arch}.deb'
        strm, stat = container.get_archive(os.path.join('/', deb_file_name))
        print(stat)
        tar_file_name = os.path.join('debs', f'{deb_file_name}.tar')
        with open(tar_file_name, 'wb') as f:
            for chunk in strm:
                f.write(chunk)
        container.remove()

        with tarfile.open(tar_file_name) as f:
            f.extractall('debs')
        os.remove(tar_file_name)

        return os.path.join('debs', f'{deb_file_name}')

    def remove_old(self):
        repos_api = self.aptly_client.repos
        packages = repos_api.search_packages(self.aptly_repo_name)
        remove_re = re.compile(f'^.+ {self.package_name} .+ .+$')
        to_be_removed = []
        for package in packages:
            if remove_re.match(package.key):
                to_be_removed.append(package.key)
        if to_be_removed:
            repos_api.delete_packages_by_key(self.aptly_repo_name, ' '.join(to_be_removed))

    def add_new(self, deb_file_location):
        files_api = self.aptly_client.files
        repos_api = self.aptly_client.repos
        uploaded_files = files_api.upload(self.aptly_repo_name, deb_file_location)
        for uploaded_file in uploaded_files:
            res = repos_api.add_uploaded_file(self.aptly_repo_name, uploaded_file)
            print(res)

    def create_new_snapshot(self):
        snapshots_api = self.aptly_client.snapshots
        all_snapshots = snapshots_api.list()
        all_snapshots.sort(key=lambda x: x.created_at, reverse=True)
        new_snaphost_name = None
        snapshot_name_re = re.compile('^socialtag-(?P<major>\d+).(?P<minor>\d+)$')

        for snapshot in all_snapshots:
            m = snapshot_name_re.match(snapshot.name)
            if m:
                latest_snapshot = snapshot
                major_version, minor_version = int(m.group('major')), int(m.group('minor'))
                minor_version += 1
                new_snaphost_name = f'socialtag-{major_version}.{minor_version}'
                break
        snapshots_api.create_from_repo(self.aptly_repo_name, new_snaphost_name)
        print(new_snaphost_name)
        return new_snaphost_name

    def publish_new_spanshot(self, new_snaphost_name):
        # print(new_snaphost_name)
        # publish_api = self.aptly_client.publish
        # res = publish_api.update(
        #     snapshots=[{'Name': new_snaphost_name}],
        #     prefix='s3:repo.socialtag.tv:beta/',
        #     distribution='vankman'
        # )
        print(f'aptly -gpg-key=730878BE36688D52 -config=./aptly.conf publish switch vankman s3:repo.socialtag.tv:beta/ {new_snaphost_name}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('package_name')
    parser.add_argument('new_version')
    parser.add_argument('--no-pull', action='store_false', dest='pull', default=True)
    parser.add_argument('--remove-old', action='store_true', dest='remove_old', default=False)
    args = parser.parse_args()

    docker_client = docker.from_env()
    aptly_client = aptly_api.Client('http://127.0.0.1:8080')

    release = Release(args.package_name, args.new_version, docker_client, aptly_client)
    
    deb_file_location = release.fetch(args.pull)
    if args.remove_old:
        release.remove_old()
    release.add_new(deb_file_location)
    new_snaphost_name = release.create_new_snapshot()
    release.publish_new_spanshot(new_snaphost_name)
