from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class AlbumSearch(FlaskForm):
    album = StringField('Album Name', validators=[DataRequired()])
