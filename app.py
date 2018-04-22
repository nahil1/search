from threading import Lock, Event

from flask import Flask, render_template, url_for, redirect, flash, request
from flask_socketio import SocketIO

from deezer import search, get_tracks, execute, set_settings, get_settings, progress_check
from forms import AlbumSearch, SettingsForm

app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = 'vgdfhgudhfguhrdughufhgkjfdayzghidreghrfudihgurigh'

thread = None
thread_lock = Lock()
end_event = Event()


@app.route('/', methods=["GET", "POST"])
def index():
    form = AlbumSearch()
    if form.validate_on_submit():
        return redirect(
            url_for('search_result', search_type=str(form.search_type.data), search_term=str(form.search_term.data)))
    return render_template('index.html', form=form)


@app.route('/search_result/<search_type>/<search_term>')
def search_result(search_type, search_term):
    if not (search_term and search_type):
        flash('You need to search for something before we can show results')
        return redirect(url_for('index'))
    data = search(search_type, search_term)
    if data:
        return render_template('search_result.html', term=search_term, data=data)
    else:
        flash('No data was returned for that search term')
        return redirect(url_for('index'))


@app.route('/tracklist/<type>/<name>/<id>')
def tracklist(type, name, id):
    tracks = get_tracks(type, id)
    if not tracks:
        flash('No data reurned for that tracklist')
        return redirect(request.referrer)
    return render_template('tracklist.html', term=name, data=tracks)


@app.route('/album/<name>/<id>')
def albums(name, id):
    flash('feature not implemented yet')
    return redirect(url_for('index'))


@app.route('/get/<media_type>/<id>')
def get(media_type, id):
    result = execute(media_type, id)
    if result == 'success':
        flash('Execute Started')
    elif result == 'no setup':
        flash('Please enter execute instructions in settings')
    return redirect(request.referrer)


@app.route('/settings', methods=["GET", "POST"])
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        set_settings(form.path.data, form.command.data, str(form.websettings.data), form.progress_file.data)
    path, command, websettings, progress_file = get_settings()
    if websettings.lower() == "false":
        flash('websettings have been disabled, please edit config.ini on the server directly')
        return redirect(url_for("index"))
    return render_template('settings.html', form=form, path=path, command=command, websettings=websettings,
                           progress_file=progress_file)


def background_thread():
    count = 0
    while True:
        socketio.sleep(1)
        data = progress_check()
        for line in data:
            socketio.emit('my_response',
                          {'data': '{}'.format(line), 'count': count},
                          namespace='/progress_check')
            count += 1


@socketio.on('connect', namespace='/progress_check')
def test_connect():
    global thread
    print('connected')
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    socketio.run(app)
