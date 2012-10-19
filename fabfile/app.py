from fabfile.utils import do
from fabfile.virtualenv import venv_path


def run():
    """Start app in debug mode (for development)."""
    do('%s/bin/python manage.py runserver' % venv_path)
