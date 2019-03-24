from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class SongForm(FlaskForm):
    songName = StringField('Name', validators=[DataRequired()])
    albumName = StringField('Album')
    author = StringField('Author', validators=[DataRequired()])
    songUrl = StringField('Song URL', validators=[DataRequired()])
    cover = StringField('Album cover URL', validators=[DataRequired()])
    sendForm = SubmitField('Upload')