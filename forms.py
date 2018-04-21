from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, RadioField
from wtforms.validators import DataRequired


class AlbumSearch(FlaskForm):
    search_type = RadioField('type', choices=[('track', 'Track'), ('album', 'Album'), ('artist', 'Artist'),
                                              ('playlist', 'Playlist')])
    search_term = StringField('Album Name', validators=[DataRequired()])


class SettingsForm(FlaskForm):
    path = StringField('path', validators=[DataRequired()])
    command = StringField('command', validators=[DataRequired()])
    websettings = BooleanField('websettings')
