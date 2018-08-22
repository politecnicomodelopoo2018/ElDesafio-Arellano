from classDB import *
from flask import *
DB().setConnection('127.0.0.1', 'root', 'alumno', 'ElDesafio')

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def Index():
    return redirect("/paginaPrincipal")


@app.route('/paginaPrincipal')
def PaginaPrincipal():
    return render_template("paginaPrincipal.html")






if __name__ == '__main__':  # para actualizar automaticamente la pagina sin tener que cerrarla
    app.run(debug=True) # para correr la pagina se puede hacer en este caso "python3 PruebaFlask.py" en la terminal