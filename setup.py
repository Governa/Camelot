#!/usr/bin/env python
import os
import camelot
from setuptools import setup, find_packages

README = os.path.join(os.path.dirname(__file__), 'readme.txt')
long_description = open(README).read() + '\n\n'

setup(
    name = 'Camelot',
    version = camelot.__version__,
    description = 'A python GUI framework on top of Sqlalchemy, Elixir and PyQt, inspired by the Django admin interface. Start building desktop applications at warp speed, simply by adding some additional information to you model definition.',
    long_description = long_description,
    keywords = 'qt pyqt sqlalchemy elixir desktop gui framework',
    author = 'Conceptive Engineering',
    author_email = 'project-camelot@conceptive.be',
    maintainer = 'Conceptive Engineering',
    maintainer_email = 'project-camelot@conceptive.be',  
    url = 'http://www.python-camelot.com',
    include_package_data = True,
    package_data = {
        # If any package contains *.txt files, include them:
        '':['*.txt', '*.rst', '*.html', '*.js', '*.png', '*.doc', '*.GPL'],
        'doc':['*.rst', '*.html', '*.png'],
    },
    license = 'GPL, Commercial',
    platforms = 'Linux, Windows, OS X',
    install_requires = ['SQLAlchemy>=0.5.6',
                        'Elixir>=0.6.1',
                        'sqlalchemy-migrate>=0.5.3',
                        'pyExcelerator>=0.6.4a',
                        'Jinja>=1.2',
                        'chardet>=1.0.1', 
                        'Babel>=0.9.4' ],
    entry_points = {'console_scripts':[
                     'camelot_admin = camelot.bin.camelot_admin:main',
                     'camelot_manage = camelot.bin.camelot_manage:main',
                    ]
                    },
    classifiers=[
              'Development Status :: 5 - Production/Stable',
              'Environment :: Win32 (MS Windows)',
              'Environment :: X11 Applications',
              'Environment :: X11 Applications :: Gnome',
              'Environment :: X11 Applications :: GTK',
              'Environment :: X11 Applications :: KDE',
              'Environment :: X11 Applications :: Qt',
              'Intended Audience :: Developers',
              'License :: OSI Approved :: GNU General Public License (GPL)',
              'License :: Other/Proprietary License',
              'Operating System :: MacOS :: MacOS X',
              'Operating System :: Microsoft :: Windows',
              'Operating System :: POSIX',
              'Programming Language :: Python',
              'Topic :: Database :: Front-Ends',
              'Topic :: Office/Business',
              'Topic :: Software Development :: Libraries :: Application Frameworks',
              ],         
    packages = find_packages() + ['doc',] )

