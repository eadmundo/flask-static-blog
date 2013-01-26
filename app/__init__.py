from werkzeug.routing import BaseConverter

from flask import Flask

from app.helpers import slugify

DEFAULT_BLUEPRINTS = [
    ('blog', '/flask-static-blog/frozen'),
]


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


def create_app(config=None, blueprints=None):
    """
    Create and initialise the application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('%s/config/default.py' % app.root_path)
    app.url_map.converters['regex'] = RegexConverter

    app.add_template_filter(slugify)

    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    configure_blueprints(app, blueprints)

    return app


def configure_blueprints(app, blueprints):
    """
    Register blueprints.
    """
    for blueprint in blueprints:
        # Import blueprint from view module
        module = __import__('app.blueprints.%s.views' % blueprint[0], globals(), locals(), '*')
        app.register_blueprint(module.blueprint, url_prefix=blueprint[1])
