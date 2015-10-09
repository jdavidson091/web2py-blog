import datetime


@auth.requires_login()
def home():
    blog_posts = db(db.blog_post.author_user_id == auth.user.id).select()
    return {'blog_posts': blog_posts}


def blog_post():
    current_post = []
    comments = []
    author_name = ""

    if len(request.args) != 1:
        response.flash = 'Invalid number of args passed for blog post'
        redirect(URL('home'))
    try:
        current_post = db(db.blog_post.id == request.args[0]).select().first()
        author = db.auth_user(db.auth_user.id == current_post.author_user_id)
        author_name = '%s %s' % (author.first_name, author.last_name)
        comments = db(db.blog_comment.blog_post_id == current_post.id).select()

    except Exception as e:
        response.flash = str(e)
        redirect(URL('home'))

    return {'current_post': current_post,
            'author': author_name,
            'comments': comments,
            # 'form': form,
            }


def new_comment():
    if auth.is_logged_in():
        current_post_id = int(request.env.http_referer[-1])

        form = SQLFORM(db.blog_comment,
                       fields=['body'],
                       labels={'body': 'Comment:'},
                       )
        form.vars.author_user_id = auth.user.id
        form.vars.blog_post_id = current_post_id
        form.vars.created_date = datetime.datetime.now()

        if form.process(keepvalues=True).accepted:
            response.flash = 'Comment posted, refresh page'
            response.js = "jQuery('#%s').hide()" % request.cid
        return dict(form=form)
    else:
        return {}


@auth.requires_login()
def new_post():
    form = SQLFORM(db.blog_post,
                   fields=['title', 'body'],
                   labels={'title': 'Post Title:',
                           'body': 'Content:'},
                   )
    form.vars.author_user_id = auth.user.id
    form.vars.created_date = datetime.datetime.now()

    form.add_button('Back', URL('home'))

    # validate_form(form)
    if form.process(keepvalues=True).accepted:
        redirect('home')
    return dict(form=form)