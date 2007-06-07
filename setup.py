from distutils.core import setup

setup(name='huTools',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      url='http://www.hosted-projects.com/trac/hudora/public/wiki', # /huTools',
      version='0.2',
      description='various tools and toys to make Python coding more fun',
      license='BSD',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python'],
      
      package_dir = {'huTools': ''},
      packages = ['huTools', 'huTools.calendar'],
      # This seems to be broken with certain Python versions:
      #package_data = {
      #      # If any package contains *.txt or *.rst files, include them:
      #      '': ['*.txt', '*.rst'],
      #},
)
