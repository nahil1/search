from flask import Flask, render_template, url_for, redirect, flash, request

from deezer import search, execute, set_settings, get_settings
from forms import AlbumSearch, SettingsForm

app = Flask(__name__)
app.secret_key = 'vgdfhgudhfguhrdughufhgkjfdayzghidreghrfudihgurigh'


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


@app.route('/tracklist/<name>/<id>')
def tracklist(name, id):
    pass


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
        set_settings(form.path.data, form.command.data, str(form.websettings.data))
    path, command, websettings = get_settings()
    if websettings.lower() == "false":
        flash('websettings have been disabled, please edit config.ini on the server directly')
        return redirect(url_for("index"))
    return render_template('settings.html', form=form, path=path, command=command, websettings=websettings)


if __name__ == '__main__':
    app.run()
