from flask import Flask, render_template, request, redirect, url_for
from models import db
from models import Students, Faculties, Points
from flask_wtf.csrf import CSRFProtect
import secrets
from forms import RegistrationForm

"""
# task1
Создать базу данных для хранения информации о студентах университета.
База данных должна содержать две таблицы: "Студенты" и "Факультеты".
В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, возраст, пол, группа и id факультета.
В таблице "Факультеты" должны быть следующие поля: id и название факультета.
Необходимо создать связь между таблицами "Студенты" и "Факультеты".
Написать функцию-обработчик, которая будет выводить список всех студентов с указанием их факультета.
###
Доработаем задача про студентов
Создать базу данных для хранения информации о студентах и их оценках в учебном заведении. 
База данных должна содержать две таблицы: "Студенты" и "Оценки". 
В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, группа и email. 
В таблице "Оценки" должны быть следующие поля: id, id студента, название предмета и оценка. 
Необходимо создать связь между таблицами "Студенты" и "Оценки". 
Написать функцию-обработчик, которая будет выводить список всех студентов с указанием их оценок.
"""

"""
# task2
Создайте форму регистрации пользователя с использованием Flask-WTF. Форма должна
содержать следующие поля:
○ Имя пользователя (обязательное поле)
○ Электронная почта (обязательное поле, с валидацией на корректность ввода email)
○ Пароль (обязательное поле, с валидацией на минимальную длину пароля)
○ Подтверждение пароля (обязательное поле, с валидацией на совпадение с паролем)
После отправки формы данные должны сохраняться в базе данных (можно использовать SQLite)
и выводиться сообщение об успешной регистрации. Если какое-то из обязательных полей не
заполнено или данные не прошли валидацию, то должно выводиться соответствующее
сообщение об ошибке.
Дополнительно: добавьте проверку на уникальность имени пользователя и электронной почты в
базе данных. Если такой пользователь уже зарегистрирован, то должно выводиться сообщение
об ошибке.
"""


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # database will be in 'instance directory
db.init_app(app)
app_secret = secrets.token_hex()
app.secret_key = app_secret
csrf = CSRFProtect(app)


@app.route('/')
def index():
    return "Hi!"


@app.route('/students/')
def list_students():
    students = Students.query.all()
    # for student in students:
    #     student.faculty = Faculties.query.filter_by(id=student.faculty_id).first().name
    #     del student.faculty_id
    # Faculties.query.filter_by(id=1).first().name # student.faculty_id -> faculty_name
    # faculties = Faculties.query.all()
    # print(123)
    # content = {'users': users}
    return render_template('table.html', students=students)


@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # if form.validate_on_submit():
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        # import hashlib
        # password = hashlib.sha256(form.password.data.encode(encoding='UTF-8')).hexdigest() # not store plain passwords
        password = form.password.data
        print(username, email, password)
        student = Students(name=form.username.data,
                           surname=form.password.data,  # sic!, but i'm lazy to update model
                           email=form.email.data,
                           age=6, gender="n", group="yes", faculty_id=1)
        db.session.add(student)
        db.session.commit()
        return redirect(url_for('register'))
    return render_template('register.html', form=form)


# for this to work need to do in console `flask init-db`
# use wsgi.py to point on your app or use `--app 'path/to/app.py'` in flask command
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DB created")


@app.cli.command("add-student")
def add_student():
    db.session.add(Students(name="s3", surname="ss3", email="my@mail.co",
                            age=6, gender="f", group="yes", faculty_id=2))
    db.session.commit()
    print("done")


if __name__ == '__main__':
    app.run()
