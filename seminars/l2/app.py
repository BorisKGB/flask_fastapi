from flask import Flask, render_template, request, abort, redirect
from werkzeug.utils import secure_filename  # sanitize requested file name
from pathlib import PurePath, Path

app = Flask(__name__)

t1 = """Создать страницу, на которой будет кнопка "Нажми меня",
при нажатии на которую будет переход на другую страницу
с приветствием пользователя по имени."""


@app.route('/task1_btn/')
def t1_btn():
    return render_template("t1_btn.html")


@app.route('/task1_hello/')
def t1_hello():
    return render_template("t1_hello.html")


t2 = """Создать страницу, на которой будет изображение и ссылка
на другую страницу, на которой будет отображаться форма
для загрузки изображений."""


@app.route('/t2_image/')
def t2_image():
    return render_template("t2_image.html")


@app.get('/t2_img_form/')
def t2_img_form_get():
    return render_template("t2_img_form.html")


@app.post('/t2_img_form/')
def t2_img_form_post():
    file = request.files.get('file')
    file_name = secure_filename(file.filename)
    file.save(PurePath.joinpath(Path.cwd(), 'uploads', file_name))
    return f"file {file_name} uploaded"


t3 = """Создать страницу, на которой будет форма для ввода логина
и пароля
При нажатии на кнопку "Отправить" будет произведена
проверка соответствия логина и пароля и переход на
страницу приветствия пользователя или страницу с
ошибкой.
"""


@app.route('/t3_form/')
def t3_form():
    return render_template("t3_form.html")


@app.post('/t3_auth/')
def t3_auth():
    users = {
        'u1': '123',
        'u2': '456'
    }
    login = request.form.get('login')
    password = request.form.get('password')
    if login in users.keys() and users[login] == password:
        return f"Hello {login}\n"

    #abort(401)
    return f"Incorrect auth data", 401


t4 = """Создать страницу, на которой будет форма для ввода текста и
кнопка "Отправить"
При нажатии кнопки будет произведен подсчет количества слов
в тексте и переход на страницу с результатом."""


@app.route('/t4_form/')
def t4_form():
    return render_template("t4_form.html")


@app.post('/t4_str_len/')
def t4_str_len():
    data = request.form.get('text')
    if data:
        return f"Вы ввели {len(data.split())} слов\n"
    # abort(404)
    return f"Incorrect data", 404


t5 = """Создать страницу, на которой будет форма для ввода двух
чисел и выбор операции (сложение, вычитание, умножение или деление) и кнопка "Вычислить"
При нажатии на кнопку будет произведено вычисление
результата выбранной операции и переход на страницу с
результатом."""


@app.route('/t5_form/')
def t5_form():
    return render_template("t5_form.html")


@app.post('/t5_calculator/')
def t5_calculator():
    num1 = request.form.get('num1')
    num2 = request.form.get('num2')
    operation = request.form.get('operation')
    allowed_operations = ['+', '-', '*', '/']
    print(num1, num2, operation)
    if num1 and num2 and num1.isnumeric() and num2.isnumeric() and operation in allowed_operations:
        num1 = int(num1)
        num2 = int(num2)
        if operation == '+':
            result = num1 + num2
        elif operation == '-':
            result = num1 - num2
        elif operation == '*':
            result = num1 * num2
        else:
            result = num1 / num2
        return f"{num1} {operation} {num2} = {result}"
    # abort(404)
    return f"Incorrect data", 404


t6 = """Создать страницу, на которой будет форма для ввода имени
и возраста пользователя и кнопка "Отправить"
При нажатии на кнопку будет произведена проверка
возраста и переход на страницу с результатом или на
страницу с ошибкой в случае некорректного возраста."""


@app.route('/t6_form/')
def t6_form():
    return render_template("t6_form.html")


@app.post('t6_user_check')
def t6_user_check():
    data = request.form.get('text')
    if data:
        return f"Вы ввели {len(data.split())} слов\n"
    return f"Incorrect data", 404


if __name__ == '__main__':
    app.run()
