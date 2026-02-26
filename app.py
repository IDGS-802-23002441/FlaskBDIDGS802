from flask import Flask, render_template, request, redirect, url_for
from flask import flash
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from flask import g
import forms
from flask_migrate import Migrate
from models import db
from models import Alumno

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf=CSRFProtect()
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/", methods=["GET", "POST"])
@app.route("/index")
def index():
    create_form = forms.userform2(request.form)
    alumno = Alumno.query.all()
    return render_template("index.html", form=create_form, alumno=alumno)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

@app.route("/alumnos", methods=["GET", "POST"])
def layout():
    create_form = forms.userform2(request.form)
    if request.method == 'POST':
            alum = Alumno(nombre = create_form.nombre.data,
                          apellidos = create_form.apellidos.data,
                          email = create_form.email.data,
                          telefono = create_form.telefono.data)
            db.session.add(alum)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template("Alumnos.html", form=create_form)

@app.route("/detalles", methods=["GET", "POST"])
def detalle():
    if request.method == 'GET':
        id = request.args.get('id')
        alum1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        id = alum1.id
        nombre = alum1.nombre
        apellidos = alum1.apellidos
        email = alum1.email
        telefono = alum1.telefono
    return render_template("detalles.html", id=id, nombre=nombre, apellidos=apellidos, email=email, telefono=telefono)

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.userform2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        create_form.id.data = alumn1.id
        create_form.nombre.data = alumn1.nombre
        create_form.apellidos.data = alumn1.apellidos 
        create_form.email.data = alumn1.email
        create_form.telefono.data = alumn1.telefono
    if request.method == 'POST':
        id = create_form.id.data
        alum = db.session.query(Alumno).filter(Alumno.id == id).first()
        alum.nombre = create_form.nombre.data
        alum.apellidos = create_form.apellidos.data
        alum.email = create_form.email.data
        alum.telefono = create_form.telefono.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("modificar.html", form=create_form)

@app.route("/eliminar", methods=["GET", "POST"])
def eliminar():
    create_form = forms.userform2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alum1= db.session.query(Alumno).filter(Alumno.id == id).first()
        create_form.id.data = request.args.get('id')
        create_form.nombre.data = alum1.nombre
        create_form.apellidos.data = alum1.apellidos
        create_form.email.data = alum1.email
        create_form.telefono.data = alum1.telefono

    if request.method == 'POST':
        id = create_form.id.data
        alum1 = Alumno.query.get(id)
        db.session.delete(alum1)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template("eliminar.html", form=create_form)


if __name__ == '__main__':
    csrf.init_app(app)
    
    with app.app_context():
        db.create_all()
    app.run(debug=True)
