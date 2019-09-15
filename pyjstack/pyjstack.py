#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019 Sarath Kumar Sivan, https://github.com/sarathkumarsivan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
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
import paramiko

from sysconfig import set_logging_console
from paramiko import SSHClient
from scp import SCPClient
from datetime import datetime
from ._version import __version__

# Logger instance for pyjstack.
logging_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logger = set_logging_console(logging.getLogger('pyjstack'), logging_format)

tempdir = tempfile.gettempdir()
workspace = '{tempdir}/pyjstack-{uuid}'.format(tempdir = tempdir, uuid = uuid.uuid4())


def setup():
    """
    Setup all the resources, directories and filesystem at the start of execution.

    :param: None
    :returns: None
    :raises: None
    """
    logger.debug('Setting up temporary workspace: %s', workspace)
    make_dirs(workspace)


def cleanup():
    """
    Cleanup all the resources, directories and filesystem at the end of execution.

    :param: None
    :returns: None
    :raises: None
    """
    logger.debug('Cleaning up temporary workspace: %s', workspace)
    shutil.rmtree(workspace)


def make_dirs(path):
    """
    Create a leaf directory and all intermediate ones. Ignores the error
    if the give path (absolute path) exists on the local file system.

    :param (str) path: None
    :returns: None
    :raises: None
    """
    try:
        os.makedirs(path)
    except OSError as err:
        if err.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def find_process(name):
    """
    Find the list of processes running on the current node by process name. It uses
    the ps Unix command to access information about processes running on your system.
    Using the -f option for ps you can gain additional useful information on each
    process in the listing: username (UID), process ID (PID), parent process ID (PPID)
    and full command lines (not just the process name).

    :param: name: Process name to be searched on your system to list the processes
    :returns: output: The console output contains the process details.
    :raises: None
    """
    session = subprocess.Popen(
        "ps -eaf | grep {name}".format(name=name), shell=True, stdout=subprocess.PIPE)
    output = session.stdout.read()
    session.stdout.close()
    session.wait()
    return output


def find_java_process():
    """
    Find the list of Java processes running on the current node.

    :param: None
    :returns: output: The console output contains the process details.
    :raises: None
    """
    return find_process('java')


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
        help='Delay in between collecting thread dumps (in seconds)')
    parser.add_argument(
        '--force', required=False,
        help='Force a stack dump when jstack [-l] pid does not respond.')
    parser.add_argument(
        '--user', required=False,
        help='Owner of the Java process')
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
        help='Email password for logging in')
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
    parser.add_argument(
        '--sftp-host', required=False,
        help='SFTP Hostname for shipping thread dump')
    parser.add_argument(
        '--sftp-port', required=False, default=22, type=int,
        help='SFTP Hostname for shipping thread dump')
    parser.add_argument(
        '--sftp-user', required=False,
        help='SFTP username for authentication')
    parser.add_argument(
        '--sftp-password', required=False,
        help='SFTP password for authentication')
    version = 'pyjstack {version}'.format(version=__version__)
    parser.add_argument('--version', action='version', version=version)
    options = parser.parse_args(args)
    return options


def jstack(options):
    """
    Get the Java stack traces of Java threads for a given Java process or
    core file or a remote debug server.

    :param: options: options to collect the stack trace.
    :returns: Java stack traces of Java threads for a given Java process.
    :raises: None
    """
    path = '{workspace}/jstack.{pid}.$(date +%\s.%N)'.format(workspace=workspace, pid=options.pid)
    logger.debug('path: %s', path)
    command = 'sudo -u {user} jstack -l {pid} > {path}'.format(user=options.user, pid=options.pid, path=path)
    status = os.system(command)
    logger.debug('status: %s', status)

    if status != 0:
        logger.debug('Forcing to collect the stack trace')
        command = 'sudo -u {user} jstack -F -l {pid} > {path}'.format(user=options.user, pid=options.pid, path=path)
        logger.debug('status: %s', status)


def make_tarfile(output_filename, source_dir):
    """
    Make the tar file for packaging all the collected Java thread dumps.

    :param: output_filename: The output filename of the target thread dump.
    :param: source_dir: The directory to which the file has to be created.
    :returns: None
    :raises: None
    """
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def execute(options):
    """
    Execute the jstack command to collect the Java thread dumps.

    :param: options: The options or parameters supplied from command-line.
    :returns: None
    :raises: None
    """
    java_version, javac_version = check_java_version()
    logger.debug('%s', java_version)
    logger.debug('%s', javac_version)

    count = options.count
    while count > 0:
        logger.debug('Running instance: %s', count)
        jstack(options)
        time.sleep(options.delay)
        count -= 1
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    archive = 'jstack-{pid}-{timestamp}.tar.gz'.format(pid=options.pid, timestamp=timestamp)
    logger.debug('Creating archive %s from %s', archive, workspace)
    make_tarfile(archive, workspace)
    size = sizeof(archive)
    path = os.path.abspath(archive)
    logger.info('Done, count: %s [Filename: %s, Size on Disk: %s, Path: %s]', count, archive, size, path)


def sizeof(filename):
    """
    Get the size of the file in human readable format.

    :param: filename: Name or absolute path of the file.
    :returns: size of the file in human readable format.
    :raises: None
    """
    if os.path.isfile(filename):
        file_info = os.stat(filename)
        return to_bytes(file_info.st_size)


def to_bytes(num):
    """
    Convert the long value of file size in human readable format.

    :param: num: The long value to be converted into bytes
    :returns: size of the file in human readable format.
    :raises: None
    """
    kb = 1024.0
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < kb:
            return "%3.1f %s" % (num, x)
        num /= kb


def check_java_version():
    """
    Check the java (JRE) and javac (JDK) version on the system.

    :param: None
    :returns: java (JRE) and javac (JDK) version on the system.
    :raises: None
    """
    java_version = subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT)
    javac_version = subprocess.check_output(['javac', '-version'], stderr=subprocess.STDOUT)
    return java_version, javac_version


def create_ssh_client(host, port, user, password):
    """
    Create an SSH client instance using paramiko. Make sure the SSH service
    should be up and running on the remote host to establish the connection.

    :param: host: The remote server to run SSH
    :param: port: The remote server port to run SSH
    :param: user: Username to login to remote server through SSH.
    :param: password: Password to login to remote server through SSH.
    :returns: java (JRE) and javac (JDK) version on the system.
    :raises: None
    """
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, user, password)
    return client


def scp(host, port, user, password, source, destination):
    """
    Copies files between hosts on a network. It uses ssh(1) for data transfer,
    and uses the same authentication and provides the same security as ssh(1).

    :param: host: Hostname or IP Address of the remote server.
    :param: port: SSH port, default is 22
    :param: user: Username to login to remote server through SSH.
    :param: password: Password to login to remote server through SSH.
    :param: source: Absolute path of the source file to copy
    :param: destination: Destination directory path on the remote server.
    :returns: None
    :raises: None
    """
    ssh = create_ssh_client(host, port, user, password)
    scp = SCPClient(ssh.get_transport())
    scp.put(source, destination)
    scp.close()


def main():
    """
    Main entry point to start the execution of thread dump collection.

    :param: None
    :returns: None
    :raises: None
    """
    start_time = time.time()  # assumes that task takes at least a tenth of second to run.
    options = get_options(sys.argv[1:])
    logger.setLevel(level=options.logging_level)
    logger.setLevel(level=logging.DEBUG)
    setup()
    logger.info("options: %s", options)

    if not options.pid:
        logger.info("Finding all the Java processes")
        print(find_java_process())
        pid = input("Which process would you like to choose?: ")
        options.pid = pid

    execute(options)
    cleanup()
    logger.info("Task completed in %s seconds" % (time.time() - start_time))


if __name__ == '__main__':
    main()