#!/usr/bin/env python3

import bottle as btl
from bottle import request, response, redirect
from beaker.middleware import SessionMiddleware

import annotate
import annotate.files as files

session_opts = {
    'session.type': 'cookie',
    'session.cookie_expires': True,
    'session.timeout': 1800,
    'session.key': 'session',
    'session.validate_key': 'qwCGyzCN0H9sNwTnk7tZOKKxQxHjLxkh',
    'session.auto': True,
}

app = btl.Bottle()

wsgi_app = SessionMiddleware(app, session_opts)

@app.get('/')
def root():
    redirect('/annotate')


@app.get('/login')
@btl.view('login')
def login_get():
    session = request.environ.get('beaker.session')
    error = session.get('error', None)
    if error is not None:
        del session['error']
        if error['code'] == 'invalid':
            return dict(invalid_name=error['name'])
    if 'name' in session:
        btl.redirect('/logged-in')


@app.post('/login')
def login_post():
    name = request.forms.getunicode('name')
    valid = annotate.user_exists(name)
    session = request.environ.get('beaker.session')
    if valid:
        session['name'] = name
        redirect_to = '/logged-in'
    else:
        session['error'] = {'code': 'invalid', 'name': name}
        redirect_to = '/login'
    btl.redirect(redirect_to)


@app.get('/logout')
def logout():
    session = request.environ.get('beaker.session')
    if 'name' in session:
        del session['name']
    btl.redirect('/login')


@app.get('/logged-in')
@btl.view('logged_in')
def logged_in():
    session = request.environ.get('beaker.session')
    name = session.get('name')
    if name is None:
        btl.redirect('/login')
    return {
        'name': name,
        'stats': files.user_stats(name)
    }


@app.get('/annotate')
def annotate_next():
    session = request.environ.get('beaker.session')
    name = session.get('name')
    if name is None:
        btl.redirect('/login')
    next_file = files.next_incomplete()
    if next_file is None:
        btl.redirect('/logged-in')
    else:
        btl.redirect('/annotate/{}'.format(next_file.id))


@app.get('/annotate/<fileid:int>')
@btl.view('annotate')
def annotate_get(fileid):
    session = request.environ.get('beaker.session')
    name = session.get('name')
    if name is None:
        btl.redirect('/login')
    context = files.around(fileid)
    if 'current' not in context:
        btl.redirect('/annotate')
    return {
        'audio': True,
        'stats': files.user_stats(name),
        'context': context
    }


@app.post('/annotate/<fileid:int>')
@btl.view('annotate')
def annotate_post(fileid):
    session = request.environ.get('beaker.session')
    name = session.get('name')
    if name is None:
        btl.redirect('/login')
    f = files.load_file(fileid)
    if f:
        annotation = request.forms.getunicode('annotation', '').strip()
        if annotation == '':
            btl.redirect('/annotate/{}'.format(fileid))
        f.annotation = annotation
        first_save = not f.complete
        f.save(name)
        if first_save and f.id % annotate.BACKUP_EVERY_N == 0:
            annotate.backup_database()
    else:
        btl.redirect('/annotate')
    btl.redirect('/annotate/{}'.format(fileid+1))


@app.get('/static/<filepath:path>')
def asset(filepath):
    return btl.static_file(filepath, root='static')


btl.run(wsgi_app, host='localhost', port=8080,
        debug=True, reloader=True)
