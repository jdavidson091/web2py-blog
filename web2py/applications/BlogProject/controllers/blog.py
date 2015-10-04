def home():
    return {'a': 'Hello World'}


def blog_post():
    b = db(db.blog_post.id == 1).select()
    c = None

    return {'blog_post': b,
            'comments': c}


def new_post():
    new_post_form = SQLFORM(db.blog_post,
                            fields=['title', 'body'],
                            labels={'title': 'Post Title:',
                                    'body': 'Content:'},
                            _action=URL('blog_post')
                            )
    # form.add_button('Back', URL('other_page'))

    validate_form(new_post_form)
    # if new_post_form.process(keepvalues=True).accepted:
    #     redirect('blog_post')
    return dict(form=new_post_form)


def validate_form(blog_post_form):
    if blog_post_form.accepts(request, session):
        response.flash = 'form accepted'
    elif blog_post_form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'