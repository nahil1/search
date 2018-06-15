from threading import Lock, Event
from flask import Flask, render_template, url_for, redirect, flash, request
from flask_socketio import SocketIO
from flask_login import LoginManager, current_user, login_user, login_required
from uuid import uuid4

from config import set_settings, get_settings
from deezer import search, get_tracks, execute, progress_check
from forms import AlbumSearch, SettingsForm, LoginForm
from user import User


app = Flask(__name__)
socketio = SocketIO(app)
app.secret_key = str(uuid4())
login = LoginManager(app)
login.login_view = 'login'


thread = None
thread_lock = Lock()
end_event = Event()


@login.user_loader
def load_user(id):
    return User()


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


@app.route('/tracklist/<item_type>/<name>/<item_id>')
def tracklist(item_type, name, item_id):
    tracks = get_tracks(item_type, item_id)
    if not tracks:
        flash('No data reurned for that tracklist')
        return redirect(request.referrer)
    print(tracks)
    return render_template('tracklist.html', term=name, data=tracks)


@app.route('/album/<name>/<item_id>')
def albums(name, item_id):
    flash('feature not implemented yet')
    return redirect(url_for('index'))


@app.route('/get/<media_type>/<item_id>')
def get(media_type, item_id):
    result = execute(media_type, item_id)
    if result == 'success':
        flash('Execute Started')
    elif result == 'no setup':
        flash('Please enter execute instructions in settings')
    return redirect(request.referrer)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if not get_settings('password'):
        form = LoginForm()
        if form.validate_on_submit():
            user = User()
            user.set_password(form.password.data)
            login_user(user)
            flash('Password Set')
            return redirect(request.args.get('next') or url_for('index'))
        return render_template('login.html', form=form, set_pass=True)

    if current_user.is_authenticated:
        flash('Already Logged in')
        return redirect(url_for('settings'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        if user.check_pasword(form.password.data):
            login_user(user)
            flash('Login Success')
            return redirect(request.args.get('next') or url_for('index'))
        else:
            flash('Login Failed')
    return render_template('login.html', form=form)


@app.route('/settings', methods=["GET", "POST"])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        set_settings(path=form.path.data, command=form.command.data, websettings=str(form.websettings.data), progress_file=form.progress_file.data)
    path, command, websettings, progress_file = get_settings('path', 'command', 'websettings', 'progress_file')
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
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target=background_thread)


if __name__ == '__main__':
    socketio.run(app)
