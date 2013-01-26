from fabfile.utils import do
from fabfile.virtualenv import venv_path


def run():
    """Start app in debug mode (for development)."""
    do('%s/bin/python manage.py runserver' % venv_path)


def freeze():
    """Build app as static site"""
    do('export FLASK_CONFIG=config/dev.py && %s/bin/python manage.py freeze' % venv_path)


def serve_frozen():
    """Serve static site up on development server"""
    do('export FLASK_CONFIG=config/dev.py && %s/bin/python manage.py serve_frozen' % venv_path)

def gh_pages():
	do('git checkout gh-pages')
	do('cp -r frozen/flask-static-blog/* .')
	do('rm -rf frozen/flask-static-blog/')
	do('git commit -am "fab test"')
	do('git push -f origin gh-pages')
	do('git checkout master')
