Account Status Parser
######################

A demo script for fetching account statuses from an API based on CSV input.

Setup
=====

*Note: This script requires Python 3*

To use, create and activate a Python 3 virtualenv: 

    ``$ virtualenv --python python3 env``

    ``$ source env/bin/activate``

From within the env, install dependencies:

    ``$ pip install -r requirements.txt`` 

Usage
======

From within the project's virtualenv, run the script:

    ``$ ./runparser -i input.csv --url http://www.foo.com/api/``

Where "input.csv" is a CSV file in the current directory, and ``--url`` is
given a valid URL to the status API.

By default, the output will be a file "output.csv" placed in the current
directory: if this file already exists, use ``--overwrite`` to replace it.
Optionally, you can also specify an output path with ``-o "myoutputfile.csv"``.

This script assumes the input uses "utf-8" character encoding. To specify a
different encoding, use ``--encoding <some valid encoding>``.

Testing
========

Unit tests are located in ``accountparser/tests``. 

To run tests against multiple versions of Python 3, use Tox. If Tox is not
already installed on the system, you can install it with:

    ``$ pip install --user tox``

With Tox installed, from within the project root do:

    ``$ tox``

Alternatively, to run tests only against the virtualenv's Python version,
use py.test from within the project's virtualenv:

    ``$ pip install pytest``

    ``$ py.test``

Libraries Used
===============

This script uses the 3rd-party Python library "Requests". In addition, the
following standard library modules are used:

    * *csv*
    * *os*
    * *sys*
    * *logging*
    * *urllib*
    * *argparse*
    * *time*

Notes
=====

Some points of consideration for future improvements:

* *config*: instead of passing in things like API URL via command line, an
  external config (e.g., yaml) could be used to set common options for
  production.

* *validation*: for now, this script does minimal input validation. There's
  plenty of room for improvement here: a good first step would be to grab all
  valid accounts in a single call to ``/accounts``, then pre-check input rows
  for valid account IDs. Invalid rows should not generate a hit against API.

* *logging*: logging is quick & dirty, and just uses the default root logger:
  this isn't optimal for any usage in production alongside other modules in the
  same logging space. 
