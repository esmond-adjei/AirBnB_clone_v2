#!/usr/bin/python3
# cleans web static archives
from fabric.api import run, local, hosts, env
import os

env.hosts = ['18.207.233.152', '100.26.221.176']


def do_clean(number=0):
    """
    Deletes out-of-date archives from the versions and releases folders
    """
    if number == 0 or number == 1:
        number = 1
    else:
        number = int(number)

    local_archives = local('ls -1t versions', capture=True).split('\n')
    remote_archives = run('ls -1t /data/web_static/releases').split('\n')

    with hosts(env.hosts):
        local('mkdir -p versions')
        for archive in local_archives[number:]:
            local('rm -f versions/{}'.format(archive))

        with cd('/data/web_static/releases'):
            for archive in remote_archives[number:]:
                run('rm -rf {}'.format(archive))

    print("Cleaned archives successfully!")
