from flask import Flask, render_template, request
import secrets
# from flask_wtf import FlaskForm, CSRFProtect
from flask_wtf.csrf import CSRFProtect
from wtform_forms import LoginForm, RegisterForm, RegistrationForm

app = Flask(__name__)
app_secret = secrets.token_hex()
app.secret_key = app_secret
# app.config['SECRET_KEY'] = app_secret
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return 'Hi'


# dummy method, needed for base template
@app.route('/data/')
def data():
    return 'data'


@app.route('/form/', methods=['GET', 'POST'])
@csrf.exempt  # disable csrf protection
def my_form():
    return 'No CSRF protection'


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        # do something with data
        pass
    return render_template('login.html', form=form)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        # do something with data
        email = form.email.data
        password = form.password.data
        print(email, password)
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run()
