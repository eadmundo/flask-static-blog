import re
import translitcodec  # provides the lookup for translit/long
from string import capwords
from math import ceil


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.]+')


def slugify(text, delim=u'-'):
    """Generates an ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = word.encode('translit/long')
        if word:
            result.append(word)
    return unicode(delim.join(result))


def deslugify(slug, delim=u'-'):
    """Turns an ASCII-only slug into human readable title"""
    return ' '.join(capwords(slug, delim).split(delim))


class Pagination(object):
    """
    Pagination class from here: http://flask.pocoo.org/snippets/44/
    """

    def __init__(self, page, per_page, total_count, items):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count
        self.items = items

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num
