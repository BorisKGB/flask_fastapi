import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
База данных должна содержать две таблицы: "Студенты" и "Факультеты".
В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, возраст, пол, группа и id факультета.
В таблице "Факультеты" должны быть следующие поля: id и название факультета.
Необходимо создать связь между таблицами "Студенты" и "Факультеты".
###
База данных должна содержать две таблицы: "Студенты" и "Оценки". 
В таблице "Студенты" должны быть следующие поля: id, имя, фамилия, группа и email. 
В таблице "Оценки" должны быть следующие поля: id, id студента, название предмета и оценка. 
Необходимо создать связь между таблицами "Студенты" и "Оценки". 
"""


class GenderEnum(enum.Enum):
    m = "m"
    f = "f"
    n = "no"


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120))
    age = db.Column(db.Integer, nullable=False)
    # gender = db.Column(db.Enum(GenderEnum), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    # ? gender = db.Column(db.Enum("m", "f", "n"))
    # ? db.Column(db.Enum("AutoService", "Insurance", "CarWash", name="service_category"))
    group = db.Column(db.String(4), nullable=False)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    points = db.relationship('Points', backref='points', lazy=True)


class Faculties(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    students = db.relationship('Students', backref='faculty', lazy=True)  # this will create faculty field in Students objects, so you can directly ask for related table columns


class Points(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    class_name = db.Column(db.String(80), nullable=False)
    point = db.Column(db.Integer, nullable=False)
