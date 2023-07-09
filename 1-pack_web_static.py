#!/usr/bin/python3
# A fabric script that generates a `.tgz` archive
#  from the web_static folder using `do_pack` funciton.
import os
from datetime import datetime
from fabric.api import local


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
