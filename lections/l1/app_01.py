from flask import Flask
from flask import render_template

app = Flask(__name__)


# string(default)|int|float|path|uuid
# @app.route('/file/<path:file>/')
# @app.route('/<float:num>/')
# multiple decoration allowed
@app.route('/')
@app.route('/<name>/')
def hi(name: str = "user"):
    return f"Hello {name}"


@app.route('/index/')
def index():
    data = {
        'title': "title",
        "name": "name"
    }
    return render_template('index.html', **data)


if __name__ == '__main__':
    app.run()
    # or in console
    # $ flask --app lections/l1/app_01.py run
