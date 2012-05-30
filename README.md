# Django Kraken Project Generator

Copyright (C) Kenneth Falck <kennu@iki.fi> 2012

The django-kraken.py script is an opinionated project generator for easy creation and installation of Django projects.

There are two main modes of using django-kraken.

## Creating a new project

To create a new project, run this anywhere:

    django-kraken.py <projectname>

The script will create the project directory, create a new virtualenv and install the requirements.

## Installing an existing project for local development

To install the necessary requirements of an existing project, run this in the project directory:

    django-kraken.py (with no arguments)

The script will auto-detect that you are in a project directory (which contains a requirements.txt file)
and install the requirements. It will also create a virtualenv for the project using virtualenvwrapper.

## Project directory layout

Generated projects use a layout familiar from Heroku:

    projectname (main project directory)
    |
    +--conf (Linux configuration files directory)
    |  |
    |  +--projectname (Nginx virtual site configuration file)
    |     projectname.conf (Gunicorn Upstart service configuration file)
    |
    +--requirements.txt (PyPi requirements)
    |
    +--projectname (Django project directory)
       |
       +--settings.py
          manage.py
          etc.

## For more information

To see full help about the options, run:

    django-kraken.py --help

