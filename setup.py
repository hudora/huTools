from setuptools import setup, find_packages

setup(name='huTools',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      url='https://cybernetics.hudora.biz/projects/wiki/huTools/',
      version='0.39p1',
      description='Various tiny tools and toys to make Python coding less work more fun.',
      long_description='''huTools is a collection of many totally non earth shattering modules:
      Various tiny tools and toys to make Python coding less work more fun. 
      See https://cybernetics.hudora.biz/projects/wiki/huTools/ for further Information.''',
      license='BSD',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python'],
      packages = find_packages(),
      zip_safe = False,
      install_requires=['decorator', 'simplejson>2.0'], 
      )
