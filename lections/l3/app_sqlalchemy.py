from flask import Flask, render_template, jsonify
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_models import db
from sqlalchemy_models import User, Post, Comment  # objects unused in code, but needed for sqlalchemy parser
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'  # database will be in 'instance directory
# need external module for connect to sql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://login:passwd@hostname/db_name'  # pymysql
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://login:passwd@hostname/db_name'  # psycopg2
# db = SQLAlchemy(app)
db.init_app(app)


@app.route('/')
def index():
    return "Hi!"


# for this to work need to do in console `flask init-db`
# use wsgi.py to point on your app or use `--app 'path/to/app.py'` in flask command
@app.cli.command("init-db")
def init_db():
    db.create_all()
    print("DB created")


@app.cli.command("add-john")
def add_user():
    user = User(username='john', email='john@example.com')
    db.session.add(user)
    db.session.commit()  # flush data to DB (commit)
    print('John added to DB')


@app.cli.command("edit-john")
def edit_user():
    user = User.query.filter_by(username='john').first()  # something like `select * from user where username = 'john' limit 1;`
    user.email = 'new_email@example.com'
    db.session.commit()
    print('John edited')


@app.cli.command("del-john")
def del_user():
    user = User.query.filter_by(username='john').first()
    db.session.delete(user)
    db.session.commit()
    print('no John anymore')


@app.cli.command("fill-db")
def fill_tables():
    count = 5
    for user in range(1, count + 1):
        new_user = User(username=f'user{user}', email=f'user{user}@mail.ru')
        db.session.add(new_user)
    db.session.commit()

    for post in range(1, count ** 2):
        author = User.query.filter_by(username=f'user{post % count + 1}').first()
        new_post = Post(title=f'Post title {post}', content=f'Post content {post}', author=author)
        db.session.add(new_post)
    db.session.commit()


@app.route('/data/')
def data():
    return 'data will be here'


@app.route('/users/')
def all_users():
    users = User.query.all()  # something like `select * from users;`
    content = {'users': users}
    return render_template('users.html', **content)


@app.route('/users/<username>/')
def users_by_name(username):
    users = User.query.filter(User.username == username).all()  # filter records
    content = {'users': users}
    return render_template('users.html', **content)


@app.route('/posts/author/<int:user_id>/')
def get_posts_by_author(user_id):
    posts = Post.query.filter_by(author_id=user_id).all()
    if posts:
        return jsonify(
            [{'id': post.id, 'title': post.title,
              'content': post.content, 'created_at': post.created_at}
             for post in posts]
        )
    else:
        return jsonify({'error': 'Posts not found'}), 404


@app.route('/posts/last-week/')
def get_posts_last_week():
    date = datetime.utcnow() - timedelta(days=7)
    posts = Post.query.filter(Post.created_at >= date).all()
    if posts:
        return jsonify(
            [{'id': post.id, 'title': post.title,
              'content': post.content, 'created_at': post.created_at}
             for post in posts]
        )
    else:
        return jsonify({'error': 'Posts not found'}), 404


if __name__ == '__main__':
    app.run()
