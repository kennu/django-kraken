#!/usr/bin/env python
# This script autogenerates a new Django project using the specified settings.
# Run django-kraken.py --help for more information.
from __future__ import print_function
import sys
import getopt
import os
import subprocess
import shutil
import re
import random

PROJECT_NAME = None
VIRTUALENV_VERSION = None
HAS_VIRTUALENVWRAPPER = False

# Available true/false options. The default is true if the option beings with 'no-'.
AVAILABLE_OPTIONS = {
    '--no-conf': "%(o)s             : Don't generate Linux configuration files in conf directory",
    '--no-gunicorn': "%(o)s         : Don't install gunicorn (WSGI server)",
    '--no-extensions': "%(o)s       : Don't install django-extensions",
    '--no-mediagenerator': "%(o)s   : Don't install django-mediagenerator",
    '--no-gravatar': "%(o)s         : Don't install django-gravatar",
    '--no-registration': "%(o)s     : Don't install django-registration",
    '--no-facebook': "%(o)s         : Don't install django-facebook",
    '--no-social-auth': "%(o)s      : Don't install django-social-auth",
    '--no-bootstrap': "%(o)s        : Don't install Twitter Bootstrap files",
    '--no-jquery': "%(o)s           : Don't install jQuery files",
    '--no-gitignore': "%(s)s        : Don't add a .gitignore file to the project",
    '--overwrite': "%(s)s           : Overwrite existing project (will delete everything first)",
}

# Available parameter options. The default value is the second value of the tuple.
AVAILABLE_PARAMS = {
    '--db':("%(o)s <engine>         : Select database engine to use (mongodb, mysql, default: %(d)s)", 'mongodb'),
    '--virtualenv':("%(o)s <name>   : Set name of virtualenv to use (default: project name)", None),
    '--workon-home':("%(o)s <path>  : Set basepath of virtualenvs (default: $WORKON_HOME or ~/.virtualenvs)", None),
    '--path':("%(o)s <path>         : Set project path (default: project name in current directory)", None),
    '--template':("%(o)s <path>     : Set project template path (default: built-in)", None),
}

# Which PyPI packages are needed always
BASE_PACKAGES = [
    'django',
]

# Which additional PyPI packages are needed for each config option
OPTIONAL_PACKAGES = {
    'gunicorn': ['gunicorn'],
    'extensions': ['django-extensions'],
    'mediagenerator': ['django-mediagenerator'],
    'gravatar': ['django-gravatar'],
    'registration': ['django-registration'],
    'facebook': ['django-facebook'],
    'social-auth': ['django-social-auth'],
}

# Which additional PyPI packages are needed for each database engine
DB_PACKAGES = {
    'mongodb': ['django-nonrel', 'djangotoolbox', 'django-mongodb-engine', 'django-mongom2m', 'pymongo'],
    'mysql': ['mysql-python'],
}

# Package version specifiers. Default is no version.
PACKAGE_VERSIONS = {
    'pymongo': '<2.2',
}

# Package URLs for packages that are not in PyPI
PACKAGE_URLS = {
    'djangotoolbox': 'hg+https://bitbucket.org/wkornewald/djangotoolbox',
    'django-nonrel': 'hg+https://bitbucket.org/wkornewald/django-nonrel',
    'django-mongodb-engine': 'git+https://github.com/django-nonrel/mongodb-engine',
    'django-mongom2m': 'git+git://github.com/kennu/django-mongom2m.git',
}

ACTIVE_OPTIONS = dict([(opt[5:], True) if opt.startswith('--no-') else (opt[2:], False) for opt, doc in AVAILABLE_OPTIONS.items()])
ACTIVE_PARAMS = dict([(opt[2:], default) for opt, (doc, default) in AVAILABLE_PARAMS.items()])

# Template variables to expand.
TEMPLATE_VARIABLES = {
    'project_name': '',
    'admins': '',
    'time_zone': '',
    'site_id': '',
    'db_engine': '',
    'db_name': '',
    'db_user': '',
    'db_password': '',
    'db_host': '',
    'db_port': '',
    'secret_key': '',
    'template_context_processors': '',
    'middleware_classes': '',
    'installed_apps': '',
    'append_slash': 'APPEND_SLASH = False',
}

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
    # Check if the directory already exists and if it contains something
    if os.path.exists(ACTIVE_PARAMS['path']):
        if len([f for f in os.listdir(ACTIVE_PARAMS['path']) if f not in ('requirements.txt',)]) > 0:
            if ACTIVE_OPTIONS['overwrite']:
                print('Completely removing old project directory %s' % ACTIVE_PARAMS['path'])
                shutil.rmtree(ACTIVE_PARAMS['path'])
            else:
                print('Project directory already exists and is not empty: %s' % ACTIVE_PARAMS['path'])
                print('Please remove it or specify another project directory with --path or change the project name.')
                return False
    if not os.path.exists(ACTIVE_PARAMS['path']):
        # Create project directory
        print('Created %s' % ACTIVE_PARAMS['path'])
        os.mkdir(ACTIVE_PARAMS['path'])
    # Now we have the project directory and it's OK to write in it. We'll also change into it.
    os.chdir(ACTIVE_PARAMS['path'])
    return True

def create_virtualenv():
    # Create base directory if it doesn't exist yet
    if not os.path.exists(ACTIVE_PARAMS['workon-home']):
        print('Creating virtualenv base directory %s' % ACTIVE_PARAMS['workon-home'])
        os.mkdirs(ACTIVE_PARAMS['workon-home'])
    virtualenv_path = os.path.join(ACTIVE_PARAMS['workon-home'], ACTIVE_PARAMS['virtualenv'])
    if os.path.exists(virtualenv_path):
        # Virtualenv already exists
        print('Using existing virtualenv: %s' % virtualenv_path)
        return True
    else:
        # Create virtualenv
        try:
            subprocess.check_call('virtualenv %s' % virtualenv_path, shell=True)
        except subprocess.CalledProcessError:
            # Failed
            print('Failed to create virtualenv, aborting.')
            return False
        print('Successfully created virtualenv: %s' % virtualenv_path)
    return True

def create_requirements():
    # Combine the base packages, optional packages and db packages
    packages = [] + BASE_PACKAGES + DB_PACKAGES[ACTIVE_PARAMS['db']]
    for opt, opt_packages in OPTIONAL_PACKAGES.items():
        if ACTIVE_OPTIONS[opt]:
            packages += opt_packages
    with open(os.path.join(ACTIVE_PARAMS['path'], 'requirements.txt'), 'w') as f:
        for package in packages:
            line = '%s%s\n' % ('-e %s#egg=%s' % (PACKAGE_URLS[package], package) if package in PACKAGE_URLS else package, PACKAGE_VERSIONS.get(package, ''))
            f.write(line)
    print('Successfully generated requirements.txt')
    return True

def install_requirements():
    # Install everything in requirements.txt to virtualenv
    print('Installing requirements into virtualenv')
    try:
        subprocess.check_call('%s install -r %s' % (os.path.join(ACTIVE_PARAMS['workon-home'], ACTIVE_PARAMS['virtualenv'], 'bin', 'pip'), os.path.join(ACTIVE_PARAMS['path'], 'requirements.txt')), shell=True)
    except subprocess.CalledProcessError:
        print('Failed to install requirements, aborting.')
        return False
    return True

def setup_template_variables():
    if not TEMPLATE_VARIABLES['project_name']:
        TEMPLATE_VARIABLES['project_name'] = '%s' % PROJECT_NAME
    if not TEMPLATE_VARIABLES['time_zone']:
        TEMPLATE_VARIABLES['time_zone'] = 'Europe/Helsinki'
    if not TEMPLATE_VARIABLES['site_id']:
        if ACTIVE_PARAMS['db'] == 'mongodb':
            # MongoDB needs an ObjectId string for site id
            TEMPLATE_VARIABLES['site_id'] = "'4fc6a88d8115a2d82e79bd27'"
        else:
            TEMPLATE_VARIABLES['site_id'] = "1"
    if not TEMPLATE_VARIABLES['db_engine']:
        if ACTIVE_PARAMS['db'] == 'mongodb':
            TEMPLATE_VARIABLES['db_engine'] = 'django_mongodb_engine'
        else:
            TEMPLATE_VARIABLES['db_engine'] = 'django.db.backends.mysql'
    if not TEMPLATE_VARIABLES['db_name']:
        TEMPLATE_VARIABLES['db_name'] = PROJECT_NAME
    if not TEMPLATE_VARIABLES['secret_key']:
        TEMPLATE_VARIABLES['secret_key'] = ''.join([random.choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
    if not TEMPLATE_VARIABLES['installed_apps']:
        TEMPLATE_VARIABLES['installed_apps'] = ''
    
def expand_template_variables(content):
    for key, value in TEMPLATE_VARIABLES.items():
        content = re.sub(r'\{\{ *%s *\}\}' % key, value, content)
    return content

def apply_template(source, target):
    print('Applying template %s => %s' % (source, target))
    name = os.path.basename(target)
    # Read template source
    with open(source, 'r') as f:
        content = f.read()
    # Expand variables only for dotfiles and .py files
    if name.startswith('.') or name.endswith('.py'):
        content = expand_template_variables(content)
    # Make sure target directory exists
    dirname = os.path.dirname(target)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    # Write target content
    with open(target, 'w') as f:
        f.write(content)
    return True

def apply_templates(template_path, project_path):
    for template in os.listdir(template_path):
        source = os.path.join(template_path, template)
        target = os.path.join(project_path, PROJECT_NAME if template == 'project_name' else template)
        if os.path.isdir(source):
            # Apply templates in subdir
            apply_templates(source, target)
        else:
            apply_template(source, target)
    return True

def create_django_project():
    # Create the Django project inside the project path. We can't use --template yet because we support Django 1.3.
    try:
        subprocess.check_call('%s startproject %s' % (os.path.join(ACTIVE_PARAMS['workon-home'], ACTIVE_PARAMS['virtualenv'], 'bin', 'django-admin.py'), PROJECT_NAME), shell=True)
    except subprocess.CalledProcessError:
        print('Failed to generate Django project, aborting.')
        return False
    # Django project generated.
    print('Successfully generated Django project: %s' % PROJECT_NAME)
    apply_templates(ACTIVE_PARAMS['template'], ACTIVE_PARAMS['path'])
    return True

def create_project():
    print_info()
    print('')
    print('Creating project %s' % PROJECT_NAME)
    print('')
    print('Enabled options:')
    print('  %s' % (' '.join([opt for opt, value in ACTIVE_OPTIONS.items() if value])))
    print('')
    print('Active parameters:')
    for opt, value in ACTIVE_PARAMS.items():
        print('  %s: %s' % (opt, value))
    print('')
    print('Template variables:')
    for opt, value in TEMPLATE_VARIABLES.items():
        print('  %s: %s' % (opt, value))
    print('')
    
    # Project generation steps:
    
    # 1. Create project directory
    if not create_project_directory(): return
    
    # 2. Create virtualenv
    if not create_virtualenv(): return

    # 3. Create requirements.txt
    if not create_requirements(): return
    
    # 4. Install the PyPI packages in requirements.txt
    if not install_requirements(): return
    
    # 5. Create the Django project
    if not create_django_project(): return

def check_kraken_requirements():
    global VIRTUALENV_VERSION, HAS_VIRTUALENVWRAPPER
    
    # To run Django Kraken, virtualenv must be already installed.
    try:
        VIRTUALENV_VERSION = subprocess.check_output('virtualenv --version', shell=True).strip()
    except subprocess.CalledProcessError:
        print('')
        print('You must have virtualenv installed to use django-kraken. The simplest way to install it on your local computer is to run:')
        print('')
        print('    sudo pip install virtualenv virtualenvwrapper')
        print('')
        print('Note: Using virtualenvwrapper might need some additional installation in your shell profile. Please Google for help.')
        print('However, django-kraken will work even if you don\'t use virtualenvwrapper, but it is recommended.')
        print('')
        print('If you are on a Debian or Ubuntu system, you probably want to install system packages instead, by running:')
        print('')
        print('    sudo apt-get install python-virtualenv virtualenvwrapper')
        print('')
        return False
    
    # virtualenvwrapper is optional
    if 'WORKON_HOME' in os.environ:
        # virtualenvwrapper is also installed
        if not ACTIVE_PARAMS['workon-home']:
            ACTIVE_PARAMS['workon-home'] = os.environ['WORKON_HOME']
        HAS_VIRTUALENVWRAPPER = True
    else:
        # virtualenvwrapper is not installed, we need to simulate it
        if not ACTIVE_PARAMS['workon-home']:
            ACTIVE_PARAMS['workon-home'] = os.path.join(os.environ['HOME'], '.virtualenvs')
        print('Warning: virtualenvwrapper is not installed, using %s as default virtualenv directory.' % ACTIVE_PARAMS['workon-home'])
    return True

def main():
    global PROJECT_NAME
    
    # Parse options
    opts, args = getopt.getopt(sys.argv[1:], 'h', ['help'] + [key[2:] for key in AVAILABLE_OPTIONS.keys()])
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print_help()
            return
        elif opt in AVAILABLE_OPTIONS:
            if opt.startswith('--no-'):
                ACTIVE_OPTIONS[opt[5:]] = False
            else:
                ACTIVE_OPTIONS[opt[2:]] = True
        else:
            print('Unrecognized option %s' % opt)
    
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
    if not ACTIVE_PARAMS['template']:
        ACTIVE_PARAMS['template'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'project_template')
    
    # Check other requirements
    if not check_kraken_requirements(): return
    
    # Setup template variables based on configuration
    setup_template_variables()
    
    # Ready to start generating
    create_project()

if __name__ == '__main__':
    main()
