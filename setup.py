import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(name='huTools',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      url='http://www.hosted-projects.com/trac/hudora/public/wiki', # /huTools',
      version='0.1',
      description='various tools and toys to make Python coding more fun',
      license='BSD',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python'],
      
        packages = find_packages(),
        package_data = {
            # If any package contains *.txt or *.rst files, include them:
            '': ['*.txt', '*.rst'],
        },
      
      zip_safe = True,
)
