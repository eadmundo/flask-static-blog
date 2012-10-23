from flask import request, url_for, abort, render_template, current_app
from app.blueprints.blog import blueprint
from app.blueprints.blog.models import BlogPost


def post_url(post):
    return url_for('blog.post_render', year=post.created.strftime('%Y'), month=post.created.strftime('%m'), slug=post.slug)

blueprint.add_app_template_filter(post_url)


@blueprint.route('/')
@blueprint.route('/tags/<string:tag>/')
@blueprint.discoverable_route('/<regex("\d{4}"):year>/<regex("\d{2}"):month>/<string:slug>/')
def post_render(year=None, month=None, slug=None, tag=None):

    page = int(request.args.get('page', 1))

    query = BlogPost.query(year=year, month=month, slug=slug, current_app=current_app)

    if query.count == 1 and slug is not None:
        return render_template('single_post.jinja', post=query.all()[0])

    if year is not None and not query.count:
        abort(404)

    if tag is not None:
        query.tagged(tag)

    pagination = query.paginate(page, current_app.config.get('BLOG_POSTS_PER_PAGE', 10))

    return render_template('posts.jinja',
            pagination=pagination,
            endpoint=request.endpoint,
            view_args=request.view_args
        )
