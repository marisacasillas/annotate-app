#!/usr/bin/env python3

from beaker.middleware import SessionMiddleware
from bottle import request, response, redirect
import bottle as btl

import gettext

from annotate.choice import Choice
import annotate
import annotate.config as config
import annotate.files as files


session_opts = {
    'session.type': 'cookie',
    'session.cookie_expires': True,
    'session.timeout': 1800,
    'session.key': 'session',
    'session.validate_key': 'qwCGyzCN0H9sNwTnk7tZOKKxQxHjLxkh',
    'session.auto': True,
}

locale = gettext.translation('messages', 'locale', languages=config.LANGUAGES)
locale.install()

app = btl.Bottle()

btl.BaseTemplate.defaults.update({
    '_': locale.gettext
})

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
    next_file = files.next_unchecked(0)
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
    if context['current'] is None:
        btl.redirect('/annotate')
    context['skip_prev'] = next_file_by_mode(fileid, 'skip_prev')
    context['skip_next'] = next_file_by_mode(fileid, 'skip_next')
    return {
        'audio': True,
        'stats': files.user_stats(name),
        'context': context,
        'choices': [
            Choice('correct_utterance', options=['0', '1']),
            Choice('word_present', options=['0', '1']),
            Choice('audio_usable', options=['0', '1']),
            Choice('audio_exclusion', options=['Microphone', 'Outside', 'Speech', 'Noise-Other', 'Extra-Vocalization', 'NA']),
            Choice('onset_quality', options=['0', '1-', '2-', '3-', '4-', '+', 'S']),
            Choice('offset_quality', options=['0', '1-', '2-', '3-', '4-', '+', 'S']),
            Choice('correct_wordform', options=['0', '1']),
            Choice('correct_context', options=['0', '1']),
            Choice('correct_speaker', options=['0', '1']),
            Choice('addressee', options=['C', 'O']),
            Choice('checked', options=['0', '1']),
        ],
        'modes': Choice('mode', options=['skip_prev', 'prev', 'next', 'skip_next']),
        'mode': request.query.getunicode('mode', 'next'),
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
        f.correct_utterance = int(request.forms.getunicode('correct_utterance'))
        f.word_present = int(request.forms.getunicode('word_present'))
        f.audio_usable = int(request.forms.getunicode('audio_usable'))
        f.audio_exclusion = request.forms.getunicode('audio_exclusion')
        f.onset_quality = request.forms.getunicode('onset_quality')
        f.offset_quality = request.forms.getunicode('offset_quality')
        f.correct_wordform = int(request.forms.getunicode('correct_wordform'))
        f.correct_context = int(request.forms.getunicode('correct_context'))
        f.correct_speaker = int(request.forms.getunicode('correct_speaker'))
        f.addressee = request.forms.getunicode('addressee')
        f.checked = int(request.forms.getunicode('checked'))
        first_save = not f.checked_at
        f.save(name)
        if first_save and f.id % annotate.BACKUP_EVERY_N == 0:
            annotate.backup_database()
    else:
        btl.redirect('/annotate')
    mode = request.forms.getunicode('mode')
    f = next_file_by_mode(fileid, mode)
    if f is None:
        btl.redirect('/logged-in')
    else:
        btl.redirect(f'/annotate/{f.id}?mode={mode}')


def next_file_by_mode(fileid, mode):
    if mode == 'skip_prev':
        return files.prev_unchecked(fileid) or files.last_unchecked()
    elif mode == 'prev':
        return files.around(fileid)['prev']
    elif mode == 'next':
        return files.around(fileid)['next']
    else:
        return files.next_unchecked(fileid) or files.next_unchecked(0)


@app.get('/static/<filepath:path>')
def asset(filepath):
    return btl.static_file(filepath, root='static')


btl.run(wsgi_app, host='localhost', port=8080,
        debug=True, reloader=True)
