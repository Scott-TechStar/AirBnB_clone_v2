from fabric.api import *
from os.path import exists
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env.hosts = ['34.227.91.107', '100.25.154.95']

def do_deploy(archive_path):
    if not exists(archive_path):
        logger.error(f"Archive file {archive_path} does not exist.")
        return False

    try:
        # Extract necessary variables
        filename = archive_path.split('/')[-1]
        no_tgz = f'/data/web_static/releases/{filename.split(".")[0]}'
        tmp = f'/tmp/{filename}'

        # Upload the archive to /tmp/ on the remote server
        put(archive_path, '/tmp/')

        # Create a directory for the new release
        run(f'mkdir -p {no_tgz}')

        # Uncompress the archive to the release directory
        run(f'tar -xzf {tmp} -C {no_tgz}')

        # Delete the uploaded archive
        run(f'rm {tmp}')

        # Move files from the web_static folder to the release directory
        run(f'mv {no_tgz}/web_static/* {no_tgz}/')

        # Remove the web_static folder
        run(f'rm -rf {no_tgz}/web_static')

        # Remove the old /data/web_static/current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new /data/web_static/current symbolic link
        run(f'ln -s {no_tgz} /data/web_static/current')

        logger.info(f"New version deployed to {no_tgz}")
        return True

    except Exception as e:
        logger.error(f"Deployment failed: {str(e)}")
        return False

if __name__ == "__main__":
    archive_path = 'path_to_your_archive.tar.gz'
    if do_deploy(archive_path):
        logger.info("Deployment successful")
    else:
        logger.error("Deployment failed")
