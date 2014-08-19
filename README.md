Mezzanine on OpenShift
======================

This repository contains working [Mezzanine](http://mezzanine.jupo.org/)
installation you can use to setup your own copy of one of the best python CMS
available. Below you'll find instructions how to set it up as is. At bottom there
 are instructions how to setup Mezzanine from scratch to use on Openshift. Enjoy!


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
    git add -A
    git commit -am "My initial CMS commit"
    git push
    ```

6. Now enjoy your application under `http://<your app name>-<your domain>.dev.rhcloud.com/`.


License
-------

This code as the original [Mezzanine](http://mezzanine.jupo.org/) is licensed under [BSD License](http://www.linfo.org/bsdlicense.html).

