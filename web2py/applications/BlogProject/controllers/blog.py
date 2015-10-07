import datetime


@auth.requires_login()
def home():
    current_user = db.auth_user(db.auth_user.id == auth.user_id)
    blog_posts = db(db.blog_post.author_user == current_user.id).select()
    return {'blog_posts': blog_posts}


def blog_post():
    current_post = []
    comments = []
    author_name = ""
    # form = None
    if len(request.args) != 1:
        response.flash = 'Invalid number of args passed for blog post'
        redirect(URL('home'))
    try:
        current_post = db(db.blog_post.id == request.args[0]).select().first()
        author = db.auth_user(db.auth_user.id == current_post.author_user)
        author_name = '%s %s' % (author.first_name, author.last_name)
        # comments = db(db.blog_comment).select().first() or []

    except Exception as e:
        response.flash = str(e)
        redirect(URL('home'))

    return {'current_post': current_post,
            'author': author_name,
            'comments': comments,
            # 'form': form,
            }


def new_comment():
    current_post = request.args[0]

    form = SQLFORM(db.blog_comment,
                   fields=['body'],
                   labels={'body': 'Comment:'},
                   )
    form.vars.author_user = auth.user
    form.vars.parent_post = current_post
    form.vars.created_date = datetime.datetime.now()

    if form.process().accepted:
        response.flash = 'Thank you'
        response.js = "jQuery('#%s').hide()" % request.cid
    return dict(form=form)


@auth.requires_login()
def new_post():
    current_user = db.auth_user(db.auth_user.id == auth.user_id)
    form = SQLFORM(db.blog_post,
                   fields=['title', 'body'],
                   labels={'title': 'Post Title:',
                           'body': 'Content:'},
                   )
    form.vars.author_user = current_user.id
    form.vars.created_date = datetime.datetime.now()
    form.vars.comments = []

    form.add_button('Back', URL('home'))

    # validate_form(form)
    if form.process(keepvalues=True).accepted:
        redirect('home')
    return dict(form=form)


def validate_form(blog_post_form):
    if blog_post_form.accepts(request, session):
        response.flash = 'form accepted'
    elif blog_post_form.errors:
        response.flash = 'one or more fields are blank'
    else:
        response.flash = 'please fill the form'