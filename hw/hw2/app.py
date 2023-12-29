from flask import Flask, render_template, redirect, url_for, request, session
from secrets import token_hex as secret_key_gen

app = Flask(__name__)
app.secret_key = secret_key_gen()


@app.get('/')
def main():
    username = session.get('username')
    return render_template('main.html', username=username)


@app.get('/login')
def login_get():
    return render_template('auth.html')


@app.post('/login')
def login_post():
    login = request.form.get('login')
    email = request.form.get('email')
    session['username'] = login
    session['email'] = email
    return redirect(url_for('main'))


@app.get('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_get'))


if __name__ == '__main__':
    app.run()
