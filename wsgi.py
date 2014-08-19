#!/usr/bin/python
import os
import sys

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass
#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

import sys
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR']))
os.environ['DJANGO_SETTINGS_MODULE'] = 'cms.settings'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.7/site-packages')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
