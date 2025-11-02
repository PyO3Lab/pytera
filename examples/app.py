import os

from flask import Flask, render_template
from pytera import PyTera


template_dir = os.path.join(os.path.dirname(__file__), "..", "templates")
tera = PyTera(f"{template_dir}/*.html")

app = Flask(__name__, template_folder=os.path.abspath(template_dir))


@app.route("/")
def index():
    return tera.render_template(
        "child.html", site_name="example", user={"name": "David"}
    )


@app.route("/child")
def child():
    return render_template("child.html", site_name="example", user={"name": "David"})


@app.route("/basic_variables")
def basic_variables():
    return tera.render_template("basic_variables.html", **{"name": "Alice", "age": 30})


@app.route("/conditionals")
def conditionals():
    return tera.render_template(
        "conditionals.html", **{"user": {"name": "Bob", "is_admin": True}}
    )


@app.route("/filters")
def filters():
    return tera.render_template(
        "filters.html",
        **{
            "text": "hello world",
            "missing": None,
            "list": ["apple", "banana", "cherry", "date"],
        },
    )


@app.route("/loops")
def loops():
    return tera.render_template(
        "loops.html",
        items=[
            {"name": "Apple", "price": 1.50},
            {"name": "Banana", "price": 0.75},
            {"name": "Cherry", "price": 2.25},
        ],
    )


if __name__ == "__main__":
    app.run()
