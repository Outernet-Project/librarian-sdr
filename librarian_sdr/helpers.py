import os
import stat
import logging
import subprocess

from librarian.core.exts import ext_container as exts


ONDD_SERVICE = 'ondd'
SDR_SERVICE = 'sdr100'


def save_sdr(sdr, path):
    """
    Saves a file-like obj `sdr` at location `path` and sets file permissions.
    """
    if os.path.exists(path):
        logging.info('Replacing existing sdr binary')
    logging.debug('Saving sdr binary at path {}'.format(path))
    try:
        copy_file(sdr, path)
        # Set the executable to be world executable
        # 755 => rwxr-xr-x
        mode = stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH
        os.chmod(path, mode)
    except:
        logging.exception('Exception while saving SDR binary at {}'.format(
            path))
        raise


def restart_tuners():
    """ Restarts SDR & ONDD by restarting the processes."""
    exts.tasks.schedule(_restart_tuners)


def copy_file(src, dest_path, buff_size=2 ** 16):
    with open(dest_path, 'wb') as dest:
        while True:
            buff = src.read(buff_size)
            if not buff:
                break
            dest.write(buff)


def _restart_tuners():
    restart_service(ONDD_SERVICE)
    restart_service(SDR_SERVICE)


def restart_service(name):
    logging.debug("Restarting service: '{}'".format(name))
    try:
        exit_code = subprocess.call(['service', name, 'restart'])
    except:
        logging.exception('Exception while restarting service {}'.format(name))
        return 1
    return exit_code