#!/usr/bin/env python
# This script autogenerates a new Django project using the specified settings.
# Run django-kraken.py --help for more information.
from __future__ import print_function
import sys
import getopt
import os

PROJECT_NAME = None

# Available true/false options. The default is true if the option beings with 'no-'.
AVAILABLE_OPTIONS = {
    '--no-conf': "%(o)s            : Don't generate Linux configuration files in conf directory",
    '--no-gunicorn': "%(o)s        : Don't install gunicorn (WSGI server)",
    '--no-extensions': "%(o)s      : Don't install django-extensions",
    '--no-mediagenerator': "%(o)s  : Don't install django-mediagenerator",
    '--no-gravatar': "%(o)s        : Don't install django-gravatar",
    '--no-registration': "%(o)s    : Don't install django-registration",
    '--no-facebook': "%(o)s        : Don't install django-facebook",
    '--no-social-auth': "%(o)s     : Don't install django-social-auth",
    '--no-bootstrap': "%(o)s       : Don't install Twitter Bootstrap files",
    '--no-jquery': "%(o)s          : Don't install jQuery files",
}

# Available parameter options. The default value is the second value of the tuple.
AVAILABLE_PARAMS = {
    '--db':("%(o)s <engine>        : Select database engine to use (mongodb, mysql, default: %(d)s)", 'mongodb'),
    '--virtualenv':("%(o)s <name>  : Set name of virtualenv to use (default: project name)", None),
    '--path':("%(o)s <path>        : Set project path (default: project name in current directory)", None),
}

# Which PyPi packages are needed for each database engine
DB_PACKAGES = {
    'mongodb': ['pymongo'],
    'mysql': ['mysql-python'],
}

ACTIVE_OPTIONS = dict([(opt[5:], True) if opt.startswith('--no-') else (opt[3:], False) for opt, doc in AVAILABLE_OPTIONS.items()])
ACTIVE_PARAMS = dict([(opt[2:], default) for opt, (doc, default) in AVAILABLE_PARAMS.items()])

def print_info():
    print('Django Kraken Project Generator by Kenneth Falck <kennu@iki.fi> 2012')

def print_help():
    print_info()
    print('')
    print('Usage: django-kraken.py [options] [projectname]')
    print('')
    print('Options:')
    for opt, doc in AVAILABLE_OPTIONS.items():
        print(doc % {'o':opt})
    print('')
    print('Parameters:')
    for opt, (doc, default) in AVAILABLE_PARAMS.items():
        print(doc % {'o':opt, 'd':default})

def create_project_directory():
    pass

def create_virtualenv():
    pass

def create_requirements():
    pass

def install_requirements():
    pass

def create_project():
    print_info()
    print('')
    print('Creating Django project:')
    print('  name: %s' % PROJECT_NAME)
    print('')
    print('Enabled options:')
    print('  %s' % (' '.join([opt for opt, value in ACTIVE_OPTIONS.items() if value])))
    print('')
    print('Disabled options:')
    print('  %s' % (' '.join([opt for opt, value in ACTIVE_OPTIONS.items() if not value]) or '(none)'))
    print('')
    print('Active parameters:')
    for opt, value in ACTIVE_PARAMS.items():
        print('  %s: %s' % (opt, value))
    print('')
    
    # Project generation steps:
    
    # 1. Create project directory
    create_project_directory()
    
    # 2. Create virtualenv
    create_virtualenv()

    # 3. Create requirements.txt
    create_requirements()
    
    # 4. Install the PyPi packages in requirements.txt
    install_requirements()

def main():
    # Parse options
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'])
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
            return
    # Require project name
    if len(args) <= 0:
        print_help()
        return
    PROJECT_NAME = args.pop(0)
    # Fail if too many args specified
    if len(args) > 0:
        print_help()
        return
    # Default virtualenv name to project name
    if not ACTIVE_PARAMS['virtualenv']:
        ACTIVE_PARAMS['virtualenv'] = PROJECT_NAME
    if not ACTIVE_PARAMS['path']:
        ACTIVE_PARAMS['path'] = os.path.join(os.getcwd(),  PROJECT_NAME)
    # Ready to start generating
    create_project()

if __name__ == '__main__':
    main()
