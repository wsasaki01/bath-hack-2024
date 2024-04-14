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

@app.route("/", methods=['GET', 'POST'])
def login():
    form = NameForm()
    message = ""

    if form.validate_on_submit():
        print(f"Username: {form.username.data}, Password: {form.password.data}")
        valid = True # replace this with validation
        if valid:
            # redirect to home page
            return redirect(url_for('home'))
        else:
            message = "This login is not valid. Please try again."

    return render_template('login.html', form=form, message=message)

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/generate", methods=['GET', 'POST'])
def generate():
    form = GenerateForm()

    if form.validate_on_submit():
        valid = True # replace this with validation
        if valid:
            # redirect to home page
            return redirect(url_for('view'))

    return render_template('generate.html', form=form)

@app.route("/view", methods=['GET', 'POST'])
def view():
    name = "sunflower"
    playlist = []
    for i in range(0,15):
        playlist.append(["Sunflowerasgdagvdfagfdeavgragfdscfdacgse", "Post Malone", "spotify", "apple music"])
    return render_template('view.html', name=name, playlist=playlist, len=len(playlist))

if __name__ == '__main__':
    app.run(debug=True, port=5500)