from fabfile.utils import do
from fabfile.virtualenv import venv_path
from fabric.context_managers import settings


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
	# switch branch
	do('git checkout gh-pages')
	# get rid of everything currently commited to that branch
	# except .gitignore. this won't get rid of frozen/
	# as long as it's not been commited by mistake
	do('git ls-tree gh-pages --name-only |grep -v .gitignore |xargs rm -rf')
	# copy eveything in frozen/flask-static-blog/ to the top level
	do('cp -r frozen/flask-static-blog/* .')
	# get rid of the old copies
	do('rm -rf frozen/flask-static-blog/')
	# add, add -u, commit and push
	do('git add .')
	do('git add -u')
	with settings(warn_only=True):
		do('git commit -am "fab test"')
	do('git push -f origin gh-pages')
	do('git checkout master')
