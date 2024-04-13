from flask import Flask, url_for, render_template, redirect
from flask_bootstrap import Bootstrap5

from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

from markupsafe import escape
import secrets

from forms import *

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(16)

bootstrap = Bootstrap5(app)

csrf = CSRFProtect(app)

@app.route("/index", methods=['GET', 'POST'])
def index():
    form = NameForm()
    message = ""

    if form.validate_on_submit():
        print("hello!!")
        # username.data, password.data
        valid = False # replace this with validation
        if valid:
            # redirect to home page
            pass
        else:
            message = "This login is not valid. Please try again."

    return render_template('index.html', form=form, message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5500)