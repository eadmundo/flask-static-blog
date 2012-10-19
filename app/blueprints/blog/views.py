from flask import url_for, abort, render_template
from app.blueprints.blog import blueprint


def post_url(post):
    return url_for('blog.post_render', year=post.created.strftime('%Y'), month=post.created.strftime('%m'), slug=post.slug)

blueprint.add_app_template_filter(post_url)


@blueprint.route('/')
@blueprint.route('/tags/<string:slug>/')
@blueprint.discoverable_route('/<regex("\d{4}"):year>/<regex("\d{2}"):month>/<string:slug>/')
def post_render(year=None, month=None, slug=None):

    # page = int(request.args.get('page', 1))

    posts = blueprint.fetch_posts(year=year, month=month, slug=slug)

    print posts

    if len(posts) == 1 and slug is not None:
        post = blueprint.file_post_to_obj(posts[0])
        return render_template('single_post.jinja', post=post)

    if year is not None and not len(posts):
        abort(404)

    return render_template('posts.jinja', posts=posts)
