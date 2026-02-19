from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms

from models import db
from models import Alumno

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
db.init_app(app)


@app.route("/")
@app.route("/index")
def index():
	return render_template("index.html")

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.route("/alumnos")
def layout():
	return render_template("Alumnos.html")

if __name__ == '__main__':
    csrf.init_app(app)
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)
