from setuptools import setup, find_packages

setup(name='huTools',
      maintainer='Maximillian Dornseif',
      maintainer_email='md@hudora.de',
      url='https://cybernetics.hudora.biz/projects/wiki/huTools',
      version='0.3',
      description='Various tiny tools and toys to make Python coding less work more fun.',
      long_description='''huTools is a collection of many totally non earth shattering modules:
      Various tiny tools and toys to make Python coding less work more fun:
      
      * calendar              - date based calculations and format conversions for HTTP and ATOM.
      * checksummming         - calculate various checksums including EAN/GTIN/NVE/SSCC and DPD GeoPost
      * luids                 - locally unique user-ids with strong guarantees of beeing unique.
      * printing              - access printers (very primitive)
      * ReReadingConfigParser - ConfigParser which detects changes in config files
      * unicode               - real-world unicode handling (very primitive)
      * world                 - country codes (very primitive)''',
      license='BSD',
      classifiers=['Intended Audience :: Developers',
                   'Programming Language :: Python'],
      
      package_dir = {'huTools': ''},
      packages = ['huTools', 'huTools.calendar'],
      zip_safe = False,      
      # This seems to be broken with certain Python versions:
      #package_data = {
      #      # If any package contains *.txt or *.rst files, include them:
      #      '': ['*.txt', '*.rst'],
      #},
)
