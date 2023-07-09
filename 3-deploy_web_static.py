#!/usr/bin/python3
# Creates and distributes an archive to my web servers using deploy.
import os.path
from datetime import datetime
from fabric.api import env, put, run, local

env.hosts = ['18.207.233.152', '100.26.221.176']


def do_pack():
    """
    Create a .tgz archive from web_static content.
    """
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    archive_path = f"versions/web_static_{timestamp}.tgz"

    if not os.path.exists("versions"):
        os.makedirs("versions")

    result = local("tar -czvf {} web_static".format(archive_path))
    if result.succeeded:
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers and deploys it
    """

    if not os.path.exists(archive_path):
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


def deploy():
    """Create and distribute an archive to a web server."""
    file = do_pack()
    if file is None:
        return False
    return do_deploy(file)
