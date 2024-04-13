from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NameForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(5, 40)])
    password = StringField('Password', validators=[DataRequired(), Length(5, 40)])
    submit = SubmitField('Submit')