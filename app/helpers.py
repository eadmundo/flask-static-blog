import re
import translitcodec  # provides the lookup for translit/long
from string import capwords


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
