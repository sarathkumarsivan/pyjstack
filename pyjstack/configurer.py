#!/usr/bin/env python

# Copyright (c) 2019 Sarath Kumar Sivan, https://github.com/sarathkumarsivan
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
import sys
import json

def configure_logging_console(logger, format):
    """
    Configure and enable console logging with the given format. The logging
    level must be explicitly set before the configuration or after the
    configuration from the caller.

    :param logger: Logger instance to be added to StreamHandler for console logging.
    :param format: Logging format to be added to StreamHandler for console logging.
    :returns: Logger instance after enabling console logging.
    :raises: None
    """
    formatter = logging.Formatter(format)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def configure_logging_file(logger, format, file):
    """
    Configure and enable file logging with the given format. The logging
    level must be explicitly set before the configuration or after the
    configuration from the caller.

    :param logger: Logger instance to be added to StreamHandler for file logging.
    :param format: Logging format to be added to StreamHandler for file logging.
    :param file: Logging format to be added to StreamHandler for file logging.
    :returns: Logger instance after enabling file logging.
    :raises: None
    """
    handler = logging.FileHandler(file)
    handler.setFormatter(format)
    logger.addHandler(handler)
    return logger

def read_json_conf(filename):
    """
    Read configuration file from local filesystem. The configuration file should be
    in valid JSON format.

    :param filename: The JSON file which has the configuration options.
    :returns: Configuration loaded from JSON configuration file.
    :raises: None
    """
    with open(filename) as json_conf_file:
        return json.load(json_conf_file)
    return None

def write_json_conf(filename, conf):
    """
    Write configuration options into a JSON file format. The file should be 
    written to the local filesystem. The user who runs this process should 
    have write permission on the given filesystem.

    :param filename: The JSON file which has the configuration options.
    :param conf: The configuration options to be written to the JSON file.
    :returns: None
    :raises: None
    """
    with open(filename, 'w') as json_conf_file:
        json.dump(conf, json_conf_file)