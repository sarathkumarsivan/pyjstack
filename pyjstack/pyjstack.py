import os
import errno
import uuid
import shutil
import logging
import tempfile

from configurer import configure_logging_console

# Logger instance for pyjstack.
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = configure_logging_console(logging.getLogger('pyjstack'), format)

tempdir = tempfile.gettempdir()
workspace = '{tempdir}/pyjstack-{uuid}'.format(tempdir = tempdir, uuid = uuid.uuid4())

def setup():
    logger.debug('Setting up temporary workspace: %s', workspace)
    makedirs(workspace)
    
def cleanup():
    logger.debug('Cleaning up temporary workspace: %s', workspace)
    shutil.rmtree(workspace)

def makedirs(path):
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def jstack(pid):
    path = '{workspace}/jstack.$pid.$(date +%\s.%N)'.format(workspace=workspace)
    command = 'jstack -F -m -l {pid} > {path}'.format(pid=pid, path=path)
    status = os.system(command)
    logger.debug('status: %s', status)

def main():
    logger.setLevel(level=logging.DEBUG)
    setup()
    jstack(6910)
    cleanup()

if __name__ == '__main__':
    main()