import os
from setuptools import setup, find_packages

setup(name='Mezzanine on OpenShift',
      version='1.0',
      description='Example Mezzanine CMS deploy to OpenShift PaaS',
      url='http://github.com/openshift-quickstart/mezzanine-quickstart/',
      license="BSD",
      packages=find_packages(),
      include_package_data=True,
      install_requires=open('%s/cms/requirements.txt' % os.environ['OPENSHIFT_REPO_DIR']).readlines(),
     )
