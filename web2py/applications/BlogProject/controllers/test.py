def index():
    return {'a': 'Hello World'}


@auth.requires_login()
def main():
    return dict()


def add_dog():
    f = SQLFORM(db.dog)
    return dict(dog_form=f)


def counter_example():
    if not session.counter:
        session.counter = 0
    session.counter += 1
    if session.counter > 10:
        redirect(URL('test', 'hello', vars={'name': 'Duder', 'phone': '1324415'}))

    message = 'hello Person'
    return {'message': message,
            'counter': session.counter}


def hello():
    name = request.vars.name
    phone = request.vars.phone

    return {'name': name,
            'phone': phone}