import datetime


@auth.requires_login()
def home():
    current_user = db.auth_user(db.auth_user.id == auth.user_id)
    blog_posts = db(db.blog_post.author_user == current_user.id).select()
    return {'blog_posts': blog_posts}


def blog_post():
    b = db(db.blog_post.id == 1).select()
    c = None

    return {'blog_post': b,
            'comments': c}


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

    # form.add_button('Back', URL('other_page'))

    validate_form(form)
    if form.process(keepvalues=True).accepted:
        redirect('new_post')
    return dict(form=form)


def validate_form(blog_post_form):
    if blog_post_form.accepts(request, session):
        response.flash = 'form accepted'
    elif blog_post_form.errors:
        response.flash = 'one or more fields are blank'
    else:
        response.flash = 'please fill the form'