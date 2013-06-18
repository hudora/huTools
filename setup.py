
from distutils.core import setup

version = '0.64'

setup(
    name='huTools',
    version=version,
    description='Various tiny tools and toys to make Python coding less work more fun.',
    long_description=open('README.rst', 'r').read(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
    ],
    keywords='python library',
    author='Maximillian Dornseif',
    author_email='md@hudora.de',
    url='http://hudora.github.com/huTools/',
    license='BSD',
    packages = [
        'huTools',
        'huTools.http',
        'huTools.http._httplib2',
        'huTools.calendar',
    ],
    include_package_data=True,
    test_suite='nose.collector',
    zip_safe=False,
    install_requires=[
        # -*- Install requires: -*-
        'setuptools',
        'decorator'
    ],
    entry_points="\n# -*- Entry points: -*-\n",
)
