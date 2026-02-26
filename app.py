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
                          apaterno = create_form.apaterno.data,
                          email = create_form.email.data)
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
        apaterno = alum1.apaterno
        email = alum1.email
    return render_template("detalles.html", id=id, nombre=nombre, apaterno=apaterno, email=email)

@app.route("/modificar", methods=["GET", "POST"])
def modificar():
    create_form = forms.userform2(request.form)
    if request.method == 'GET':
        id = request.args.get('id')
        alumn1 = db.session.query(Alumno).filter(Alumno.id == id).first()
        create_form.id.data = alumn1.id
        create_form.nombre.data = alumn1.nombre
        create_form.apaterno.data = alumn1.apaterno 
        create_form.email.data = alumn1.email
    if request.method == 'POST':
        id = create_form.id.data
        alum = db.session.query(Alumno).filter(Alumno.id == id).first()
        alum.nombre = create_form.nombre.data
        alum.apaterno = create_form.apaterno.data
        alum.email = create_form.email.data
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
        create_form.apaterno.data = alum1.apaterno
        create_form.email.data = alum1.email
        
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
