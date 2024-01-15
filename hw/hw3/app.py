from flask import Flask, render_template, request, redirect, url_for
from models import db, User
from flask_wtf.csrf import CSRFProtect
import secrets
from forms import RegistrationForm
from hashlib import sha256
from sqlalchemy import inspect


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
app_secret = secrets.token_hex()
app.secret_key = app_secret
csrf = CSRFProtect(app)


@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        user = User(name=form.name.data,
                    surname=form.surname.data,
                    email=form.email.data,
                    password=sha256(form.password.data.encode(encoding='UTF-8')))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


# for this to work need to do in console `flask init-db`
# use wsgi.py to point on your app or use `--app 'path/to/app.py'` in flask command
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DB created")  # TODO update to logging


def all_tables_exist() -> bool:
    """
    Validate database tables
    Does not validate columns
    :return: bool, validation result
    """
    wanted_tables = db.metadata.tables
    existed_tables = inspect(db.engine).get_table_names()
    for table_name, table_data in wanted_tables.items():
        if table_name not in existed_tables:
            return False
    return True
    # inspect(db.engine)
    # inspect(db.engine).get_table_names()
    # inspect(db.engine).get_columns('user')


if __name__ == '__main__':
    # https://stackoverflow.com/questions/30428639/check-database-schema-matches-sqlalchemy-models-on-application-startup
    with app.app_context():
        # я не осилил полноценную проверку структуры БД
        # не понял как получить wanted_table_columns в виде допустимом к сравнению с existed_table_columns
        if not all_tables_exist():
            db.create_all()
            print("Database was created")  # TODO update to logging
    app.run()
