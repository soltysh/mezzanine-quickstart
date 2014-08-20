Mezzanine on OpenShift
======================

This repository contains working [Mezzanine](http://mezzanine.jupo.org/)
installation you can use to setup your own copy of one of the best python CMS
available. Below you'll find instructions how to set it up as is. At bottom there
 are instructions how to setup Mezzanine from scratch to use on OpenShift. Enjoy!


Setup as is
-----------

Assuming you already have an [OpenShift](https://www.openshift.com/) account, if
not go immediately and [create one](https://www.openshift.com/app/account/new)!

1. Create a python-2.7 application with either mysql or postgresql db cartridge.
In following steps I'll be using postgresql cart, but one should be able to
easily switch that to mysql.

    ```
    rhc app create <your app name> python-2.7 postgresql-9.2
    ```

2. cd into the directory that matches your application name

    ```
    cd <your app name>
    ```

3. Add this git repository as an upstream to your application

    ```
    git remote add upstream -m master git://github.com/openshift-quickstart/mezzanine-quickstart.git
    ```

4. Merge this repository into your application

    ```
    git pull -s recursive -X theirs upstream master
    ```

5. In `cms/settings.py` locate `SECRET_KEY` and `NEVERCACHE_KEY` and change their
values with your own, and _DO NOT SHARE_ this value with anyone (see [Django docs]
(https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY)).
Also it might be good idea to update `TIME_ZONE` according to your demands.

6. Commit all changes and push code back to OpenShift.

    ```
    git commit -am "My initial CMS commit"
    git push
    ```

6. Now enjoy your application at `http://<your app name>-<your domain>.dev.rhcloud.com/`.


Setup Mezzanine from scratch
----------------------------

1. Create a python-2.7 application with either mysql or postgresql db cartridge.
In following steps I'll be using postgresql cart, but one should be able to
easily switch that to mysql.

    ```
    rhc app create <your app name> python-2.7 postgresql-9.2
    ```

2. cd into the directory that matches your application name

    ```
    cd <your app name>
    ```

3. Create virtual env (I'm using [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/en/latest/)
for managing my virtual environments), and install latest version of Mezzanine.

    ```
    mkvirtualenv mezzanine
    pip install Mezzanine
    ```

4. Create Mezzanine project, while being inside your OpenShift app. I'm calling
my app `cms` but you can change that name, but remember to change this value in
all other places I'm using it.

    ```
    mezzanine-project cms
    ```

5. Modify `setup.py` to reference `cms/requirements.txt` file, so you don't have
to update two requirements files.

    ```python
    import os
    from setuptools import setup, find_packages

    setup(name='YourAppName',
          version='1.0',
          description='OpenShift App',
          author='Your Name',
          author_email='example@example.com',
          url='http://www.python.org/sigs/distutils-sig/',
          packages=find_packages(),
          include_package_data=True,
          install_requires=open('%s/cms/requirements.txt' % os.environ['OPENSHIFT_REPO_DIR']).readlines(),
         )
    ```

6. Modify `wsgi.py` removing everything after IMPORTANT note and adding:

    ```python
    import sys
    sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR']))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'cms.settings'
    os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.7/site-packages')

    import django.core.handlers.wsgi
    application = django.core.handlers.wsgi.WSGIHandler()
    ```

7. Update `cms/settings.py` adding `SECRET_KEY` and `NEVERCACHE_KEY` and change
their values with your own, and _DO NOT SHARE_ this value with anyone (see [Django docs]
(https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-SECRET_KEY)).

    ```python
    SECRET_KEY = "some_very_long_random_text"
    NEVERCACHE_KEY = "yet_another_very_long_random_text"
    ```

    Next locate `DATABASES` and change it's value with:

    ```python
    import os
    import urlparse

    DATABASES = {}
    if 'OPENSHIFT_POSTGRESQL_DB_URL' in os.environ:
        url = urlparse.urlparse(os.environ.get('OPENSHIFT_POSTGRESQL_DB_URL'))
        DATABASES['default'] = {
            'ENGINE' : 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['OPENSHIFT_APP_NAME'],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
        }

    elif 'OPENSHIFT_MYSQL_DB_URL' in os.environ:
        url = urlparse.urlparse(os.environ.get('OPENSHIFT_MYSQL_DB_URL'))
        DATABASES['default'] = {
            'ENGINE' : 'django.db.backends.mysql',
            'NAME': os.environ['OPENSHIFT_APP_NAME'],
            'USER': url.username,
            'PASSWORD': url.password,
            'HOST': url.hostname,
            'PORT': url.port,
            }

    else:
        DATABASES['default'] = {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'dev.db',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    ```

    Add `.rhcloud.com` to `ALLOWED_HOSTS`:

    ```python
    ALLOWED_HOSTS = [
        '.rhcloud.com',
    ]
    ```

    Finally locate `STATIC_ROOT` and change it with:

    ```python
    if 'OPENSHIFT_REPO_DIR' in os.environ:
        STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
    else:
        STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))
    ```

    and `MEDIA_ROOT` with:

    ```python
    if 'OPENSHIFT_DATA_DIR' in os.environ:
        MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_DATA_DIR'), 'media')
    else:
        MEDIA_ROOT = os.path.join(PROJECT_ROOT, *MEDIA_URL.strip("/").split("/"))
    ```

8. One more step and you're ready to go, add `.openshift/action_hooks/build` with
following contents:

    ```bash
    #!/bin/bash

    # link media directories from data dir to be used by django upload

    if [ ! -d $OPENSHIFT_DATA_DIR/media ]; then
        mkdir $OPENSHIFT_DATA_DIR/media
    fi

    ln -sf $OPENSHIFT_DATA_DIR/media $OPENSHIFT_REPO_DIR/wsgi/static/media
    ```

    and `.openshift/action_hooks/deploy` with:

    ```bash
    #!/bin/bash

    # make sure to run db synchronization

    source ${OPENSHIFT_PYTHON_DIR}virtenv/bin/activate

    export PYTHON_EGG_CACHE=${OPENSHIFT_PYTHON_DIR}virtenv/lib/python-2.7/site-packages

    echo "Executing 'python ${OPENSHIFT_REPO_DIR}cms/manage.py syncdb --noinput'"
    python "$OPENSHIFT_REPO_DIR"cms/manage.py syncdb --noinput

    echo "Executing 'python ${OPENSHIFT_REPO_DIR}cms/manage.py collectstatic --noinput -v0'"
    python "$OPENSHIFT_REPO_DIR"cms/manage.py collectstatic --noinput -v0
    ```

    and `wsgi/static/.htaccess` with:

    ```apache
    RewriteEngine On
    RewriteRule ^application/static/(.+)$ /static/$1 [L]
    ```

    *NOTE* Don't forget to add executable rights to `.openshift/action_hooks/{deploy,build}`.

9. Commit everything and push to OpenShift and enjoy your application at
`http://<your app name>-<your domain>.dev.rhcloud.com/`.


License
-------

This code as the original [Mezzanine](http://mezzanine.jupo.org/) is licensed under [BSD License](http://www.linfo.org/bsdlicense.html).

