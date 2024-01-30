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
                    password=sha256(form.password.data.encode(encoding='UTF-8')).digest())
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
    Validate database tables and columns by names
    Does not validate column types
    :return: bool, validation result
    :raises Exception: on mismatch columns data
    """
    wanted_tables = db.metadata.tables
    db_inspector = inspect(db.engine)
    existed_tables_list = db_inspector.get_table_names()
    for table_name, table_data in wanted_tables.items():
        if table_name not in existed_tables_list:
            return False
        existed_table_columns = {el['name']: el for el in inspect(db.engine).get_columns('user')}
        for column_name, wanted_column_data in table_data.columns.items():
            if column_name not in existed_table_columns:
                raise Exception("Incorrect SQL structure, check database scheme")
            existed_column_info = dict()
            wanted_column_info = dict()
            for column_param in existed_table_columns[column_name]:
                if column_param == 'primary_key':
                    existed_column_info[column_param] = bool(existed_table_columns[column_name][column_param])
                    wanted_column_info[column_param] = wanted_tables[table_name].columns[
                        column_name].__getattribute__(column_param)
                elif column_param == 'type':
                    col_param = existed_table_columns[column_name][column_param]
                    col_len = ""
                    if "length" in existed_table_columns[column_name][column_param].__dict__:
                        col_len = str(col_param.length)
                    existed_column_info[column_param] = col_param.python_type.__name__ + col_len
                    col_param = wanted_tables[table_name].columns[column_name].__getattribute__(column_param)
                    col_len = ""
                    if "length" in wanted_tables[table_name].columns[column_name].type.__dict__:
                        col_len = str(col_param.length)
                    wanted_column_info[column_param] = col_param.python_type.__name__ + col_len
                else:
                    existed_column_info[column_param] = existed_table_columns[column_name][column_param]
                    wanted_column_info[column_param] = wanted_tables[table_name].columns[
                        column_name].__getattribute__(column_param)
            for column_param in existed_column_info:
                # ignore type parameter
                # Wanted types does not equal to Existed types
                #  String(80) -> Varchar(80) suppressed by checking python_type.__name__
                #  Decimal -> bytes(32) Do not know what to do with this yet
                if column_param != 'type' and existed_column_info[column_param] != wanted_column_info[column_param]:
                    raise Exception("Incorrect SQL structure, check database scheme")
    return True


if __name__ == '__main__':
    # https://stackoverflow.com/questions/30428639/check-database-schema-matches-sqlalchemy-models-on-application-startup
    with app.app_context():
        # я не осилил полноценную проверку структуры БД
        # могу какими-то окольными путями получить инфо о колонках, но wanted column String(length=80), а existed column Varchar(length=80)
        # пока не понимаю как это обойти
        if not all_tables_exist():
            db.create_all()
            print("Database was created")  # TODO update to logging
    app.run()
