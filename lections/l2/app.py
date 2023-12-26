from flask import Flask, render_template
from flask import request
from werkzeug.utils import secure_filename  # sanitize requested file name
from pathlib import PurePath, Path
from flask import abort
from flask import redirect
from flask import flash, get_flashed_messages  # get_flashed_messages can be used only in same method with flash
# app.secret_key must be set for usage of flash messages
from flask import make_response
from flask import session  # must be set for usage of flash messages
# sessions live through server restarts
# from flask import url_for
# url_for("test_url", num=42, data="new_data", pi=3.14515) # in code usage
# "test_url" is name of method connected to route, not route path
# and parameters must correspond method parameters
# {{ url_for("static", filename='some_file.file') }} # in template usage for generate link to something in static
# there is default method for 'static' url's
from markupsafe import escape

app = Flask(__name__)
# import secrets
# app.secret_key = secrets.token_hex()
app.secret_key = b'skjfhgskhfgsdfhflksdfhljhsdfljkdkj'  # must be set for usage of flash messages


@app.route("/")
def index():
    return "import path to file in url"


@app.route('/path/<path:file>/')
def get_file(file):
    print(file)
    # return f"your file is in: {file}" # text """<script>alert("wawawa")</script>""" lead to js inject on user side
    return f"your file is in: {escape(file)}"


# @app.route('/url_for/')
# def test_url():
#     return f"""1. {url_for("test_url")}<br>
# 2. {url_for("test_url", data="1a2b3c", pi=3.14)}<br>
# 3. {url_for("get_file", file=123, pi=3.14)}<br>
# 4. {url_for("static", filename="123.png")}<br>"""


@app.route("/test/")
def test():
    return render_template("test.html")


@app.route('/get/')
def get():
    return f"{request.args}\n"


@app.route("/submit/", methods=['GET', 'POST'])
# $ curl -X GET localhost:5000/submit
# $ curl -X POST localhost:5000/submit -F "name=123
# or u can @app.get(...) OR @app.post(...), dont forget to use different methods for each
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        if name:
            return f"Hello {name}\n"
        else:
            abort(404)  # return 404, will ask for @app.errorhandler(404) and return its result
    return render_template("test.html")


@app.route('/upload/', methods=['GET', 'POST'])
# $ curl -X GET localhost:5000/upload/
# $ curl -X POST localhost:5000/upload/ -F "file=@/tmp/403MDXM_181223_181223_D.html"
def upload():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
        return f"file {file_name} uploaded"
    return render_template("test.html")


@app.errorhandler(404)
def page_not_found(e):
    app.logger.warning(e)  # manual push log message
    return f"error {e} for {request.base_url}", 404


# we can return user fancy http/500
@app.errorhandler(500)
def global_error(e):
    app.logger.warning(e)  # manual push log message
    return f"Всё сломалось: {e} for {request.base_url}", 500


@app.route("/redirect_me/")
def redir():
    return redirect("/")
    # return redirect(url_for("get_file", file="test"))  # can also set parameters, by method url_for


@app.route('/flash_msg')
def flash_msg():
    flash("msg", "success")
    # return render_template("test2.html")
    return f"messages: {get_flashed_messages(with_categories=True)}\n"


@app.route('/cookies_set/')
# $ curl -X GET localhost:5000/cookies_set/ -I
# Set-Cookie: my_key=my_val; Path=/
def cookies_set():
    response = make_response("Cookie set")
    # you able to modify response as you need
    response.headers['my_header'] = "new-value"
    response.set_cookie('my_key', 'my_val')
    return response


@app.route('/cookies_get/')
# $ curl -X GET localhost:5000/cookies_get/ --cookie "my_key=my_val; Path=/"
# -> ImmutableMultiDict([('my_key', 'my_val'), ('Path', '/')])
def cookies_get():
    return f"{request.cookies}"


@app.route('/session_add/<name>')
# $ curl -X GET localhost:5000/session_add/bac -I
# -> Set-Cookie: session=eyJiYWMiOiJiYWMifQ.ZYm6wA.7pkahI1xExfAlIpdRV_NhXXCq5I; HttpOnly; Path=/
def new_session(name):
    session[name] = name
    return f"set session for {name}\n"


@app.route('/session_list')
# will return nothing unless there is no cookies set
# $ curl -X GET localhost:5000/session_list
# -> dict_items([])
# $ curl -X GET localhost:5000/session_list --cookie "session=eyJiYWMiOiJiYWMifQ.ZYm6wA.7pkahI1xExfAlIpdRV_NhXXCq5I; HttpOnly; Path=/"
# -> dict_items([('bac', 'bac')])
def list_sessions():
    return f"{session.items()}\n"


@app.route('/session_del/<name>')
# need to set cookies to work
# $ curl -X GET localhost:5000/session_del/bac --cookie "session=eyJiYWMiOiJiYWMifQ.ZYm6wA.7pkahI1xExfAlIpdRV_NhXXCq5I; HttpOnly; Path=/" -I
# -> Set-Cookie: session=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Max-Age=0; HttpOnly; Path=/
# it effectivly reset cookie, you still can reuse old value
def del_session(name):
    if name in session:
        session.pop(name)
    return "ok\n"


if __name__ == '__main__':
    app.run()
