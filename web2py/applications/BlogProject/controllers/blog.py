import datetime


@auth.requires_login()
def prompt_login():
    redirect(URL('home'))


def home():
    author_id = ''
    if request.args:
        author_id = request.args[0]
    elif not auth.is_logged_in():
        redirect(URL('prompt_login'))
    else:
        author_id = auth.user_id

    blog_posts = db(db.blog_post.author_user_id == author_id).select()
    return {'blog_posts': blog_posts,
            'author_id': author_id}


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
        able_to_delete_comments = False

        if auth.is_logged_in():
            if current_post.author_user_id == auth.user_id:
                able_to_delete_comments = True

    except Exception as e:
        response.flash = str(e)
        redirect(URL('home'))

    return {'current_post': current_post,
            'author': author_name,
            'comments': comments,
            'able_to_delete_comments': able_to_delete_comments,
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


@auth.requires_login()
def edit_post():
    post_to_edit_id = db.blog_post(request.args(0)) or redirect(URL('home'))
    post_to_edit = db.blog_post(db.blog_post.id == post_to_edit_id)

    form = SQLFORM(db.blog_post, post_to_edit,
                   deletable=True,
                   fields=['title', 'body'],
                   labels={'title': 'Post Title:',
                           'body': 'Content:'},
                   )
    form.process(detect_record_change=True)
    if form.record_changed:
        redirect(URL('blog_post', args=[post_to_edit_id]))
    elif form.accepted:
        redirect(URL('blog_post', args=[post_to_edit_id]))

    return dict(form=form)


@auth.requires_login()
def delete_comment():
    comment_to_delete = db.blog_comment(request.args[0]) or redirect(URL('home'))
    b_post = db.blog_post(request.args[1]) or redirect(URL('home'))

    db(db.blog_comment.id == comment_to_delete.id).delete()

    redirect(URL('blog_post', args=[b_post.id]))
