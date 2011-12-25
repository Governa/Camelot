#  ============================================================================
#
#  Copyright (C) 2007-2011 Conceptive Engineering bvba. All rights reserved.
#  www.conceptive.be / project-camelot@conceptive.be
#
#  This file is part of the Camelot Library.
#
#  This file may be used under the terms of the GNU General Public
#  License version 2.0 as published by the Free Software Foundation
#  and appearing in the file license.txt included in the packaging of
#  this file.  Please review this information to ensure GNU
#  General Public Licensing requirements will be met.
#
#  If you are unsure which license is appropriate for your use, please
#  visit www.python-camelot.com or contact project-camelot@conceptive.be
#
#  This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
#  WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#
#  For use of this library in commercial applications, please contact
#  project-camelot@conceptive.be
#
#  ============================================================================
"""
Utility functions and classes to start a new Camelot project, this
could be the start of MetaCamelot
"""

import os

from camelot.core.conf import settings
from camelot.core.utils import ugettext_lazy as _
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.object_admin import ObjectAdmin
from camelot.admin.action import Action
from camelot.view.controls import delegates

from camelot.view.main import Application

class MetaSettings(object):
    """settings target to be used within MetaCamelot, when no real
    settings are available yet"""

    CAMELOT_MEDIA_ROOT = '.'
    
    def ENGINE(self):
        return 'sqlite:///'
        
    def setup_model(self):
        pass

class MetaCamelotAdmin( ApplicationAdmin ):
    """ApplicationAdmin class to be used within meta camelot"""
    
    name = 'Meta Camelot'

def launch_meta_camelot():
    import sys
    from camelot.view.model_thread import construct_model_thread, get_model_thread
    from camelot.admin.action import GuiContext
    from PyQt4 import QtGui
    app = QtGui.QApplication([a for a in sys.argv if a])
    construct_model_thread()
    mt = get_model_thread()
    mt.start()
    settings.append( MetaSettings() )
    new_project = CreateNewProject()
    gui_context = GuiContext()
    gui_context.admin = MetaCamelotAdmin()
    new_project.gui_run( gui_context )
    # keep app alive during running of app
    return app
    
class MetaCamelotApplication( Application ):
    """A Camelot application to build new Camelot
    projects."""
    
    def initialization(self):
        new_project = CreateNewProject('New Camelot Project')
        new_project.run()

#
# The various features that can be set when creating a new Camelot project
#

features = [
   ('source',                '.',                                       delegates.LocalFileDelegate, '''The directory in which to create<br/>'''
                                                                                                     '''the sources of the new project '''),
   ('name',                  'My Application',                          delegates.PlainTextDelegate, '''The name of the application<br/>'''
                                                                                                     '''as it will appear in the main window and<br/>'''
                                                                                                     '''will be used to store settings in the<br/>'''
                                                                                                     '''registry.'''),
   ('author',                'My Company',                              delegates.PlainTextDelegate, '''The author of the application, this<br/>'''
                                                                                                     '''will be used to store settings in the<br/>'''
                                                                                                     '''registry.'''),
   ('module',                'myapplication',                           delegates.PlainTextDelegate, '''The name of the python module that<br/>'''
                                                                                                     '''will contain the application'''),
   ('domain',                'mydomain.com',                            delegates.PlainTextDelegate, '''The domain name of the author, this will<br/>'''
                                                                                                     '''be used to store settings in the registry'''),
   ('application_url',       'http://www.python-camelot.com',           delegates.PlainTextDelegate, '''Website of the application'''),
   ('help_url',              'http://www.python-camelot.com/docs.html', delegates.PlainTextDelegate, '''Part of the website with online help'''),
   ('installer',             False,                                     delegates.BoolDelegate,      '''Build a windows installer'''),
]

#
# Templates of the files to create when starting a new project
#
 
templates = [
    ('{{options.module}}/application_admin.py', '''
from camelot.view.art import Icon
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.section import Section

class MyApplicationAdmin(ApplicationAdmin):
  
    name = '{{options.name}}'
    application_url = '{{options.application_url}}'
    help_url = '{{options.help_url}}'
    author = '{{options.author}}'
    domain = '{{options.domain}}'
    
    def get_sections(self):
        from camelot.model.memento import Memento
        from camelot.model.authentication import Person, Organization
        from camelot.model.i18n import Translation
        return [ Section( 'relation',
                          self,
                          Icon('tango/22x22/apps/system-users.png'),
                          items = [Person, Organization]),
                 Section( 'configuration',
                          self,
                          Icon('tango/22x22/categories/preferences-system.png'),
                          items = [Memento, Translation])
                ]
    '''),
    
    ('__init__.py', ''),
    
    ('{{options.module}}/__init__.py', ''),

    ('{{options.module}}/test.py', '''
#
# Default unittests for a camelot application.  These unittests will create
# screenshots of all the views in the application.  Run them with this command :
#
# python -m nose.core -v -s {{options.module}}/test.py
#

import os

from camelot.test import EntityViewsTest

# screenshots will be put in this directory
static_images_path = os.path.join( os.path.dirname( __file__ ), 'images' )

class MyApplicationViewsTest( EntityViewsTest ):

    images_path = static_images_path
    '''),
    
    ('main.py', '''
import logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger('main')

def start_application():
    from camelot.view.main import main
    from {{options.module}}.application_admin import MyApplicationAdmin
    main(MyApplicationAdmin())

if __name__ == '__main__':
    start_application()
    '''),
    
    ('{{options.module}}/model.py', '''
from camelot.model import metadata

__metadata__ = metadata
    '''),
    
    ('excludes.txt', '''
vtk*
test*
sphinx*

Lib\site-packages\cvxopt*
Lib\site-packages\IPython*
Lib\site-packages\logilab*
Lib\site-packages\nose*
Lib\site-packages\PIL*
Lib\site-packages\py2exe*
Lib\site-packages\pyflakes*
Lib\site-packages\pylint*
Lib\site-packages\pytz\zoneinfo\*
Lib\site-packages\rope*
Lib\site-packages\Sphinx*
Lib\site-packages\spyder*
Lib\site-packages\unittest*
Lib\site-packages\virtualenv*
Lib\site-packages\VTK*
Lib\site-packages\docutils*
Lib\site-packages\pyreadline*
    '''),
    ('settings.py', '''
import logging
import os

logger = logging.getLogger('settings')

# media root needs to be an absolute path for the file open functions
# to function correctly
CAMELOT_MEDIA_ROOT = os.path.join(os.path.dirname(__file__), 'media')

# backup root is the directory where the default backups are stored
CAMELOT_BACKUP_ROOT = os.path.join(os.path.dirname(__file__), 'backup')

# default extension for backup files
CAMELOT_BACKUP_EXTENSION = 'db'

# template used to create and find default backups
CAMELOT_BACKUP_FILENAME_TEMPLATE = 'default-backup-%(text)s.' + CAMELOT_BACKUP_EXTENSION


def ENGINE():
    """This function should return a connection to the database"""
    from sqlalchemy import create_engine
    return create_engine('sqlite:///model-data.sqlite')

def setup_model():
    """This function will be called at application startup, it is used to setup
    the model"""
    import camelot.model
    from elixir import setup_all
    import {{options.module}}.model
    setup_all(create_tables=True)
    from camelot.model.authentication import updateLastLogin
    updateLastLogin()
    '''),
    ('setup.py', '''

#
# Default setup file for a Camelot application
#
# To build a windows installer, execute this file with :
#
#     python setup.py egg_info bdist_cloud wininst_cloud
#
# Running from the Python SDK command line
#

import datetime
import logging

from setuptools import setup, find_packages

logging.basicConfig( level=logging.INFO )

setup(
    name = '{{options.name}}',
    version = '1.0',
    author = '{{options.author}}',
    url = '{{options.application_url}}',
    include_package_data = True,
    packages = find_packages(),
    py_modules = ['settings', 'main'],
    entry_points = {'gui_scripts':[
                     'main = main:start_application',
                    ],},
    options = {
        'bdist_cloud':{'revision':'0',
                       'branch':'master',
                       'update_before_launch':False,
                       'default_entry_point':('gui_scripts','main'),
                       'changes':[],
                       'timestamp':datetime.datetime.now(),
                       },
        'wininst_cloud':{ 'excludes':'excludes.txt'},
    }, 

  )

    '''),
]

class NewProjectOptions(object):
    
    def __init__(self):
        for feature in features:
            setattr( self, feature[0], feature[1] )       

    class Admin( ObjectAdmin ):
        verbose_name = _('New project')
        form_display = [feature[0] for feature in features]
        field_attributes = dict(
            ( feature[0],{ 'editable':True,
                           'delegate':feature[2],
                           'nullable':False,
                           'tooltip':feature[3]   } ) for feature in features)
        field_attributes['source']['directory'] = True
            
class CreateNewProject( Action ):
    """Action to create a new project, based on a form with
    options the user fills in."""
            
    def model_run(self, context = None):
        # begin change object
        from PyQt4 import QtGui
        from camelot.view import action_steps
        options = NewProjectOptions()
        yield action_steps.UpdateProgress( text = 'Request information' )
        yield action_steps.ChangeObject( options )
        # end change object
        yield action_steps.UpdateProgress( text = 'Creating new project' )
        self.start_project( options )
        project_path = os.path.abspath( options.source )
        if options.installer:
            cloudlaunch_found = False
            try:
                import cloudlaunch
                cloudlaunch_found = True
            except Exception, e:
                yield action_steps.MessageBox( 'To build a Windows installer, you need to be using<br/>' \
                                               'the Conceptive Python SDK, please visit<br/>' \
                                               '<a href="http://www.conceptive.be/python-sdk.html">www.conceptive.be/python-sdk.html</a><br/>' \
                                               'for more information' )
            if cloudlaunch_found:
                yield action_steps.UpdateProgress( text = 'Building windows installer' )
                import distutils.core
                current_dir = os.getcwd()
                # change to the app directory for setuptools to do its job
                os.chdir( project_path )
                setup_path = os.path.join( 'setup.py' )
                distribution = distutils.core.run_setup( setup_path, 
                                                         script_args = ['egg_info', 'bdist_cloud', 'wininst_cloud'] )
                os.chdir( current_dir )
                for command, _python_version, filename in  distribution.dist_files:
                    if command == 'wininst_cloud':
                        yield action_steps.MessageBox( 'Use Inno Setup to process the file<br/>' \
                                                       '<b>%s</b><br/> to build the installer executable'% os.path.join( project_path, filename ),
                                                       standard_buttons = QtGui.QMessageBox.Ok )

        yield action_steps.MessageBox( 'All files for the new project<br/>' \
                                       'were created in <b>%s</b>'%project_path,
                                       standard_buttons = QtGui.QMessageBox.Ok )
        yield action_steps.OpenFile( project_path )
        
    def start_project( self, options ):
        from jinja2 import Template
        context = {'options':options}
        if not os.path.exists( os.path.join( options.source, options.module ) ):
            os.makedirs( os.path.join( options.source, options.module ) )
        for filename_template, code_template in templates:
            filename = Template( filename_template ).render( context )
            code = Template( code_template ).render( context )            
            fp = open( os.path.join( options.source, filename ), 
                       'w' )
            fp.write( code )
            fp.close()
