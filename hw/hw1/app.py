from flask import Flask, render_template

app = Flask(__name__)

shoes = []
jackets = []

menu_elements = {
    "Main": "main",
    "Clothes": "clothes",
    "Jackets": "jackets",
    "Shoes": "shoes"
}


@app.route('/')
def main(template: str = "main"):
    return render_template("main.html", page="Main", menu_elements=menu_elements)


@app.route('/clothes/', defaults={"template": "clothes.html"})
def clothes():
    pass


@app.route('/shoes/', defaults={"template": "shoes.html"})
def shoes():
    pass


@app.route('/jackets/', defaults={"template": "jackets.html"})
def jackets():
    pass


if __name__ == '__main__':
    app.run()
