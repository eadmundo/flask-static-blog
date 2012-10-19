class BlogPost(object):

    @property
    def public(self):
        return self.published or self.private

    def __init__(self, **data):

        for key, value in data.items():
            setattr(self, key, value)

    def __repr__(self):
        return '<Post %r>' % self.title
