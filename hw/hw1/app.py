from flask import Flask, render_template

app = Flask(__name__)

shoes_list = []
jackets_list = [
    {'img': 'j1.png',
     'description': 'черно-красная куртка на молнии, футболка куртка, красная куртка, молния, манжета, экипировка'},
    {'img': 'j2.png',
     'description': 'Кожаная куртка Рукав, куртка, текстиль, кожа, черный'},
    {'img': 'j3.png',
     'description': 'Куртка кожаная Куртка кожаная Куртка А-2 Летная куртка, куртка, молния, коричневый, текстиль'}
]

menu_elements = {
    "Main": "main",
    "Clothes": "clothes",
    "Jackets": "jackets",
    "Shoes": "shoes"
}


@app.route('/')
def main(template: str = "main"):
    return render_template("main.html", page="Main", menu_elements=menu_elements)


@app.route('/clothes/')
def clothes():
    return render_template("clothes.html", page="Clothes", menu_elements=menu_elements, products=[*jackets_list])


@app.route('/shoes/', defaults={"template": "shoes.html"})
def shoes():
    return render_template("main.html", page="Shoes", menu_elements=menu_elements, products=shoes_list)


@app.route('/jackets/', defaults={"template": "jackets.html"})
def jackets():
    return render_template("main.html", page="Jackets", menu_elements=menu_elements, products=jackets_list)


if __name__ == '__main__':
    app.run()
