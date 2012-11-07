from app import create_app
from flask import current_app
from flask.ext.script import Manager, Server
from flask.ext.frozen import Freezer

manager = Manager(create_app)

manager.add_command('runserver', Server(host='0.0.0.0'))


@manager.command
def freeze():
    freezer = Freezer(current_app)
    freezer.freeze()


@manager.command
def serve_frozen():
    freezer = Freezer(current_app)
    freezer.serve(host='0.0.0.0')

if __name__ == "__main__":
    manager.run()
