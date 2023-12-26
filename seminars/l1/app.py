from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)


@app.route('/')
# @app.route('/about/', defaults={"page_text": "about page"})
# @app.route('/contact/', defaults={"page_text": "contact page"})
def main(page_text=None):
    if page_text:
        return page_text
    return "Hello world"


@app.route("/sum/<int:first>/<int:second>")
def my_sum(first: int, second: int):
    return f"{first + second}"


@app.route("/str_len/<text>/")
def str_len(text: str):
    return str(len(text))


@app.route("/html/")
def html():
    return render_template("index.html")

# extra tables
import pandas as pd
from tabulate import tabulate


@app.route("/table/")
def html_table():
    data = [
        {"name": "n1", "surname": "f1", "age": 5, "avg_points": 4},
        {"name": "n2", "surname": "f2", "age": 1, "avg_points": 3},
        {"name": "n3", "surname": "f3", "age": 7, "avg_points": 5},
        {"name": "n4", "surname": "f4", "age": 3, "avg_points": 8}
    ]
    # default
    # return render_template("table.html", data=data)
    # using tabulate
    # html_table = tabulate(data, headers='keys', tablefmt='html')
    # return render_template("table.html", table=html_table)
    df_html = pd.DataFrame(data).to_html()
    return render_template("table.html", table=df_html)


@app.route("/news/")
def news():
    news = [
        {"header": "h1", "text": "balblabla", "pub_date": datetime.now()},
        {"header": "h2", "text": "balblablasdfa", "pub_date": datetime.now()}
    ]
    return render_template("news.html", news=news)


@app.route('/about/', defaults={"template": "about.html"})
@app.route('/contact/', defaults={"template": "contact.html"})
# as part task#9, reuse base.html
@app.route('/clothes/', defaults={"template": "clothes.html"})
@app.route('/shoes/', defaults={"template": "shoes.html"})
@app.route('/jacket/', defaults={"template": "jacket.html"})
def page(template: str):
    if template:
        return render_template(template)
    else:
        return "How do i get here"


if __name__ == '__main__':
    app.run()
