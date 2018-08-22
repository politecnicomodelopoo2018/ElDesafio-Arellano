from classDB import *
from flask import *
from classHilo import *
from classTag import *
from classUsuario import *
from datetime import date
DB().setConnection('127.0.0.1', 'root', 'alumno', 'ElDesafio')



app = Flask(__name__, static_url_path='/static')

@app.route('/')
def Index():
    return redirect("/paginaPrincipal")


@app.route('/paginaPrincipal')
def PaginaPrincipal():
    return render_template("paginaPrincipal.html")

@app.route('/signUp')
def LogIn():
    return render_template("signUp.html")

@app.route('/registrarUsuario', methods=['GET', 'POST'])
def Registrar():
    print("HOLAAA")
    print(request.form.get("nombre"))
    usuario = Usuario()
    usuario.setNombre(request.form.get("nombre"))
    usuario.setMail(request.form.get("mail"))
    usuario.setFechaCreacion(date.today())
    usuario.setNickName(request.form.get("nickName"))
    usuario.setApellido(request.form.get("apellido"))
    usuario.guardate()
    return render_template("/paginaPrincipal.html")

if __name__ == '__main__':  # para actualizar automaticamente la pagina sin tener que cerrarla
    app.run(debug=True) # para correr la pagina se puede hacer en este caso "python3 PruebaFlask.py" en la terminal