import os
import re
from datetime import date
from operator import attrgetter
from itertools import izip_longest
import yaml
import markdown
from app.helpers import slugify, deslugify, Pagination


class BlogPostQuery(object):

    def __init__(self, year=None, month=None, slug=None, current_app=None):

        self.regexp = '(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]{2})-(?P<slug>[0-9a-zA-Z_-]*)\.m(?:ark)?d(?:own)?'

        if year is not None:
            self.regexp = self.regexp.replace('(?P<year>[0-9]{4})', '(?P<year>%s)' % str(year))

        if month is not None:
            self.regexp = self.regexp.replace('(?P<month>[0-9]{2})', '(?P<month>%s)' % str(month))

        if slug is not None:
            self.regexp = self.regexp.replace('(?P<slug>[0-9a-zA-Z_-]*)', '(?P<slug>%s)' % str(slug))

        path = current_app.config.get('BLOG_FILE_POSTS_FOLDER', False)

        self.posts = []

        for file_name in os.listdir(path):
            m = re.match(self.regexp, file_name)
            if m:
                self.posts.append(BlogPost(**{
                    'title': deslugify(m.group('slug')),
                    'year': m.group('year'),
                    'month': m.group('month'),
                    'day': m.group('day'),
                    'slug': m.group('slug'),
                    'path': os.path.join(path, file_name),
                    'created': date(int(m.group('year')), int(m.group('month')), int(m.group('day')))
                }))

        self.posts.sort(key=attrgetter('created'), reverse=True)

    @property
    def count(self):
        return len(self.posts)

    def paginate(self, page, per_page):
        if self.count <= per_page:
            items = self.all()
        else:
            items = [post.populate() for post in list(izip_longest(*[iter(self.posts)] * per_page))[page - 1] if post is not None]
        return Pagination(page, per_page, self.count, items)

    def tagged(self, query_tag):
        tagged_posts = self.all()
        self.posts = [post for post in tagged_posts if query_tag in [slugify(tag) for tag in post.tags]]

    def all(self):
        return [post.populate() for post in self.posts if post is not None]


class BlogPost(object):

    def __init__(self, **data):

        for key, value in data.items():
            setattr(self, key, value)

    @staticmethod
    def query(year=None, month=None, slug=None, current_app=None):
        return BlogPostQuery(year=year, month=month, slug=slug, current_app=current_app)

    def populate(self):
        post_content = open(self.path, 'r').read()
        match = re.match('^\s*---\s*(.*)---\s*(.*)', post_content, re.DOTALL)
        if match is not None:
            content = markdown.markdown(match.groups()[1], ['codehilite'])
            self.content = content
            front_matter = yaml.load(match.groups()[0])
            if front_matter.get('title', None) is not None:
                self.title = front_matter.get('title')
            self.tags = front_matter.get('tags', [])
        return self

    def __repr__(self):
        return '<Post %r>' % self.title
