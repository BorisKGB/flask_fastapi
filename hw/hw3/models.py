from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    surname = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120))
    # according to
    # https://stackoverflow.com/questions/247304/what-data-type-to-use-for-hashed-password-field-and-what-length
    # SHA-256 generates a 256-bit hash value. You can use CHAR(64) or BINARY(32)
    password = db.Column(db.BINARY(32), nullable=False)
