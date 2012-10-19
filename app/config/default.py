import os

# no debugging by default - this is overriden in runserver for local dev
DEBUG = ASSETS_DEBUG = False

# override with something sensible
SECRET_KEY = 'SecretKeyForSessionSigning'

# Folder to look for file-based blog posts
BLOG_FILE_POSTS_FOLDER = os.path.realpath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'posts'))
