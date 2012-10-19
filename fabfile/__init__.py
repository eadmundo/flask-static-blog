from fabric.decorators import task

import virtualenv
import app


@task
def build():
    """
    Execute build tasks.
    """
    virtualenv.build()


@task
def run():
    """
    Run app in debug mode (for development).
    """
    app.run()
