from flask import Flask, render_template, url_for, session, redirect, flash

from deezer import search_album, execute
from forms import AlbumSearch

app = Flask(__name__)
app.secret_key = 'vgdfhgudhfguhrdughufhgkjfdayzghidreghrfudihgurigh'


@app.route('/', methods=["GET", "POST"])
def index():
    form = AlbumSearch()
    if form.validate_on_submit():
        session['search_term'] = form.album.data
        return redirect(url_for('result'))
    return render_template('index.html', form=form)


@app.route('/result')
def result():
    if not ('search_term' in session.keys()):
        flash('A search term is required to display results')
        return redirect(url_for('index'))
    term = session['search_term']
    data = search_album(term)
    if data:
        return render_template('result.html', term=term, data=data)
    else:
        flash('No data was returned for that search term')
        return redirect(url_for('index'))


@app.route('/get/<id>')
def get(id):
    result = execute(id)
    if result == 'success':
        flash('Download Success')
        return redirect(url_for('result'))
    elif result == 'no setup':
        flash('Please enter execute instructions in settings')
    return redirect(url_for('result'))


@app.route('/settings')
def settings():
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
