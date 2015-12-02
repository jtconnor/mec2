mec2
=======================

Python package to query information about the current ec2 instance.  Useful for
ec2 instances to configure themselves.

Install::

$ pip install mec2

Command line::

$ mec2 instance_id

Library::

  import mec2
  print mec2.instance_id()

View available commands in `source code
<https://github.com/jtconnor/mec2/blob/master/mec2/mec2.py>`_.

Push new version to pypi::

$ vim setup.py  # Edit version tag
$ rm -rf dist
$ python setup.py sdist
$ twine upload dist/*
