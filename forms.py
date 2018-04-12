from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AlbumSearch(FlaskForm):
    album = StringField('Album Name', validators=[DataRequired()])


class SettingsForm(FlaskForm):
    path = StringField('path', validators=[DataRequired()])
    command = StringField('command', validators=[DataRequired()])
    websettings = StringField('websettings', validators=[DataRequired()])
