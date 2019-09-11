pyjstack
========
|docs| |travis| |pypi| |coverage|

.. |docs| image:: http://img.shields.io/badge/Docs-latest-green.svg
.. |travis| image:: https://travis-ci.org/sarathkumarsivan/pyjstack.svg?branch=master
.. |pypi| image:: https://img.shields.io/pypi/v/pyjstack.svg
.. |coverage| image:: https://img.shields.io/badge/coverage-100%25-brightgreen


The pyjstack command-line tool lets you to collect the thread dump of Java processes currently running on your system. A thread dump is a snapshot of the state of all threads that are part of the process. The state of each thread is presented with a so called stack trace, which shows the contents of a thread’s stack. Some of the threads belong to the Java application you are running, while others are JVM internal threads. A thread dump reveals information about an application’s thread activity that can help you diagnose problems and better optimize application and JVM performance; for example, thread dumps automatically shows the occurrence of a deadlock. Deadlocks bring some or all of an application to a complete halt. The pyjstack uses the jstack utility to print Java stack traces. 

Most often a single thread dump will reveal the problem, this is especially true with deadlocks where two or more threads are waiting for locks obtained by each other. But in other cases, such as threads waiting on other processes, like IO from a database, you won't be able to detect it with a single thread dump. In this case multiple thread dumps taken over time will show the same thread waiting for the process to complete during that time span. The pyjstack can generate multiple thread dumps over time. Running pyjstack from the command line, the default is 12 thread dumps with a 1 second delay between each dump, this is configurable from the command line. If you are running pyjstack without the pid and there are multiple Java processes running on the machine pyjstack will detect it and get the list of pids, you have to choose the pid to generate the thread dump.

Installation
------------

The pyjstack can be installed via pip, the Python package manager. If pip isn’t already available on your system of Python, run the following commands to install it:
::

    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py --user

Then install pyjstack
::

    sudo pip install pyjstack

Install from GitHub via pip:
::

    pip install git+https://github.com/sarathkumarsivan/pyjstack.git

You can also install the latest version directly from a cloned Git repository:
::

    git clone https://github.com/sarathkumarsivan/pyjstack.git
    cd pyjstack
    python setup.py install

If you face any issue while installation related to six package, you can ignore it like this:
::

    pip install pyjstack --ignore-installed six

Upgrade
-------
You can upgrade pyjstack via pip; issue the below command to perform the upgrade:
::

    sudo pip install pyjstack --upgrade

Usage
-----
To obtain a thread dump using pyjstack, run the following command:
::

    pyjstack --pid 12397 --count 12 --delay 1 

Options
#######

**--pid:**
  The PID of your Java process. If you are running pyjstack without the pid and there are multiple Java processes running on the machine pyjstack will detect it and get the list of pids, you have to choose the pid to generate the thread dump.

**--count:**
  The count indicates how many thread dumps to take.

**--delay:**
  The delay indicates the time delay in seconds between each dump.

**--verbose:**
  Enable debug level logging. You can enable verbose logging which exactly similar to the DEBUG level. If you see any unexpected behavior while issuing pyjstack, enablling this option would be a good choice to identify the problem and trace the root cause. 

**--quiet:**
  Make little or no noise while collecting the thread dump. During the normal execution of pyjstack command, INFO level logs would be printed on the console; but if you provide --quiet option, the command would be executed silently.

Supports
--------
Tested on Python 2.7, 3.2, 3.4, 3.6, 3.7