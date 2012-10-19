import types
import os
import re
from datetime import date
from operator import attrgetter
import yaml
import markdown
from flask import Blueprint, current_app
from app.helpers import deslugify
from app.blueprints.blog.models import BlogPost


def discoverable_route(self, route, **options):
    def decorator(f):
        endpoint = options.pop('endpoint', None)
        rules = filter(None, route.split('/'))
        aggregate_route = '/'
        for rule in rules:
            aggregate_route = '%s%s/' % (aggregate_route, rule)
            self.add_url_rule(aggregate_route, endpoint, f, **options)
        return f
    return decorator

BASE_POST_REGEXP = '(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})-(?P<slug>[a-zA-Z_-]*)\.m(?:ark)?d(?:own)?'


def fetch_posts(self, year=None, month=None, slug=None):
    # our base regexp
    regexp = BASE_POST_REGEXP

    if year is not None:
        # amend our regexp to filter by year
        regexp = regexp.replace('(?P<year>[0-9]{4})', str(year))

    if month is not None:
        regexp = regexp.replace('(?P<month>[0-9]{2})', "%02d" % (int(month),))

    if slug is not None:
        regexp = regexp.replace('(?P<slug>[a-zA-Z_-]*)', str(slug))

    path = current_app.config.get('BLOG_FILE_POSTS_FOLDER', False)

    posts = []

    for file_name in os.listdir(path):
        m = re.match(regexp, file_name)
        if m:
            posts.append(BlogPost(**{
                'title': deslugify(m.group('slug')),
                'year': m.group('year'),
                'month': m.group('month'),
                'day': m.group('day'),
                'slug': m.group('slug'),
                'path': os.path.join(path, file_name),
                'created': date(int(m.group('year')), int(m.group('month')), int(m.group('day')))
            }))

    return sorted(posts, key=attrgetter('created'), reverse=True)


def populate_post(self, post):
    post_content = open(post.path, 'r').read()
    match = re.match('^\s*---\s*(.*)---\s*(.*)', post_content, re.DOTALL)
    if match is not None:
        content = markdown.markdown(match.groups()[1], ['codehilite'])
        post.content = content
        front_matter = yaml.load(match.groups()[0])
        if front_matter.get('title', None) is not None:
            post.title = front_matter.get('title')
    else:
        return False


blueprint = Blueprint('blog', __name__, template_folder='templates')

blueprint.discoverable_route = types.MethodType(discoverable_route, blueprint, Blueprint)

blueprint.fetch_posts = types.MethodType(fetch_posts, blueprint, Blueprint)

blueprint.populate_post = types.MethodType(populate_post, blueprint, Blueprint)
