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
import tarfile

from time import sleep
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
    session = subprocess.Popen(
        "ps -eaf | grep {name}".format(name=name), shell=True, stdout=subprocess.PIPE)
    output = session.stdout.read()
    session.stdout.close()
    session.wait()
    return output


def find_java_processes():
    """
    Find the list of Java processes running on the current node.

    :param: None
    :returns: output: The console output contains the process details.
    :raises: None
    """
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
        '--pid', required=False,
        help='Process ID of the Java process')
    parser.add_argument(
        '--count', required=False, default=12, type=int,
        help='Count of thread dumps to be collected')
    parser.add_argument(
        '--delay', required=False, default=1, type=int,
        help='Delay in between collecting thread dumps, (in seconds)')
    parser.add_argument(
        '--smtp-server', required=False,
        help='SMTP server for email dispatch')
    parser.add_argument(
        '--smtp-port', required=False,
        help='SMTP server port for email dispatch')
    parser.add_argument(
        '--from-email', required=False,
        help='Email From Address')
    parser.add_argument(
        '--password', required=False,
        help='Email password for loggining in')
    parser.add_argument(
        '--to-email', required=False,
        help='Email To Address')
    parser.add_argument(
        '--subject', required=False,
        help='Email subject line')
    parser.add_argument(
        '--message', required=False,
        help='Email message body or content')
    parser.add_argument(
        '--attachment', required=False,
        help='Email attachment if any')
    options = parser.parse_args(args)
    return options

def jstack(pid):
    path = '{workspace}/jstack.$pid.$(date +%\s.%N)'.format(workspace=workspace)
    command = 'jstack -F -m -l {pid} > {path}'.format(pid=pid, path=path)
    status = os.system(command)
    logger.debug('status: %s', status)

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def execute(options):
    count = options.count
    while count > 0:
        logger.debug('Runing instance: %s', count)
        jstack(options.pid)
        time.sleep(options.delay)
        count -= 1
    logger.debug('Done, count: %s', count)

def main():
    start_time = time.time()  # assumes that task takes at least a tenth of second to run.
    options = get_options(sys.argv[1:])
    logger.setLevel(level=options.logging_level)
    logger.setLevel(level=logging.DEBUG)
    setup()
    logger.info("options: %s", options)
    if options.pid:
        execute(options)
    else:
        logger.info("Finding all the Java processes")
        print(find_java_processes())
        pid = input("Which process would you like to choose?: ")
        options.pid = pid
        execute(options)
    cleanup()
    logger.info("Task completed in %s seconds" % (time.time() - start_time))

if __name__ == '__main__':
    main()