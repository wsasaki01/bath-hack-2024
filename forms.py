from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NameForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Length(1, 12)
        ],
        render_kw={
            'class':'text-input login-username teko-small',
            'placeholder':'USERNAME',
        }
    )
    password = StringField(
        'Password',
        validators=[
            DataRequired(),
            Length(1, 12)
        ],
        render_kw={
            'class':'text-input login-password teko-small',
            'placeholder':'PASSWORD',
        }
    )
    submit = SubmitField(
        'SUBMIT',
        render_kw={
            'class':'login-submit teko-small',
        }
    )

class GenerateForm(FlaskForm):
    submit = SubmitField('Generate!')