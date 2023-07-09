#!/usr/bin/python3
# Deploys source code to server
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['18.207.233.152', '100.26.221.176']


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it
    """

    if not exists(archive_path):
        return False

    try:
        filename = archive_path.split('/')[-1]
        fname = filename.split('.')[0]

        put(archive_path, '/tmp/{}'.format(filename))
        run('mkdir -p /data/web_static/releases/{}/'.format(fname))
        run('tar -xzf /tmp/{} -C'
            '/data/web_static/releases/{}/'.format(filename, fname))
        run('rm /tmp/{}'.format(filename))
        run('mv /data/web_static/releases/{}/web_static/*'
            '/data/web_static/releases/{}/'.format(fname, fname))
        run('rm -rf /data/web_static/releases/{}/web_static'.format(fname))
        run('rm -rf /data/web_static/current')
        run('ln -s /data/web_static/releases/{}/'
            '/data/web_static/current'.format(fname))

        print('New version deployed!')
        return True
    except Exception as e:
        print('Deployment failed:', e)
        return False
