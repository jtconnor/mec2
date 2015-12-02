mec2
=======================

Python package to query information about the current ec2 instance.  Useful for
ec2 instances to configure themselves.


Push new version to pypi::

$ vim setup.py  # Edit version tag
$ rm -rf dist
$ python setup.py sdist
$ twine upload dist/*

