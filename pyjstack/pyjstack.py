import os
import errno
import uuid
import shutil
import logging
import tempfile
import argparse
import sys
import time
import subprocess

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

def find_processes(name):
    ps = subprocess.Popen(
        "ps -eaf | grep {name}".format(name=name), 
        shell=True, stdout=subprocess.PIPE)
    output = ps.stdout.read()
    ps.stdout.close()
    ps.wait()
    return output

def find_java_processes():
    return find_processes('java')

def get_options(args):
    """
    Get the command-line options for executing pyjstack commands.

    :param: args
    :returns: map options: Options supplied from command-line
    :raises: None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbose', help="Enable debug level logging", action="store_const",
        dest="logging_level", const=logging.DEBUG, default=logging.INFO)
    parser.add_argument(
        '--quiet', help="Make little or no noise while taking thread dump",
        action="store_const", dest="logging_level", const=logging.CRITICAL)
    parser.add_argument(
        '--pid', required=True,
        help='Process ID of the Java process')
    options = parser.parse_args(args)
    return options

def jstack(pid):
    path = '{workspace}/jstack.$pid.$(date +%\s.%N)'.format(workspace=workspace)
    command = 'jstack -F -m -l {pid} > {path}'.format(pid=pid, path=path)
    status = os.system(command)
    logger.debug('status: %s', status)

def main():
    start_time = time.time()  # assumes that task takes at least a tenth of second to run.
    options = get_options(sys.argv[1:])
    logger.setLevel(level=options.logging_level)
    logger.setLevel(level=logging.DEBUG)
    setup()
    jstack(options.pid)
    cleanup()

if __name__ == '__main__':
    main()