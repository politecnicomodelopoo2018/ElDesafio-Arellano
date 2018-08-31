
from flask import *
from classPost import *
from classHilo import *
from datetime import date
DB().setConnection('127.0.0.1', 'root', 'alumno', 'ElDesafio')

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def Index():
    if 'userid' in session:
        return render_template("/homeUsuario.html", usuario=Usuario.getUsuario(session['userid']),
                               listaPosts=Post.getAllPosts())
    return render_template("/paginaPrincipal.html")


@app.route('/logIn')
def Login():
    if 'userid' in session:
        return redirect("/")
    return render_template("/logIn.html")


@app.route('/signUp')
def LogIn():
    return render_template("signUp.html")


@app.route('/usuarioHilos')
def UsuarioHilos():
    return render_template("/usuarioHilos.html", usuario=Usuario.getUsuario(session['userid']), ListaHilos=Hilo.hilosParaUsuario(session['userid']))


@app.route('/crearHilo')
def CrearHilo():
    return render_template("/crearHilo.html", usuario=Usuario.getUsuario(session['userid']))


@app.route('/postDeHilo')
def PostsDeHilo():
    return render_template("/postDeHilo.html", usuario=Usuario.getUsuario(session['userid']), ListaPosts=Post.postsParaHilo(int(request.args.get("idhilo"))), Hilo=Hilo.getHilo(int(request.args.get("idhilo"))))


@app.route('/crearPost')
def CrearPost():
    return render_template("/crearPost.html", Hilo=Hilo.getHilo(int(request.args.get("idhilo"))))


@app.route('/registrarUsuario', methods=['GET', 'POST'])
def Registrar():
    usuario = Usuario()
    usuario.setNombre(request.form.get("nombre"))
    usuario.setMail(request.form.get("mail"))
    usuario.setFechaCreacion(date.today())
    usuario.setNickName(request.form.get("nickName"))
    usuario.setApellido(request.form.get("apellido"))
    usuario.setContraseña(request.form.get("contraseña"))
    usuario.guardate()
    return redirect("/")


@app.route('/loginAction', methods=['GET', 'POST'])
def LoginAction():
    usuario = Usuario.getUsuarioDesdeMail(request.form.get("mail"))
    if hashlib.sha256((request.form.get("contraseña")).encode('utf-8')).hexdigest() == usuario.contraseña:
        session['userid'] = usuario.id
    return redirect("/")


@app.route('/logOut')
def logout():
   session.pop('userid', None)
   return redirect("/")


@app.route('/crearHiloAction', methods=['GET', 'POST'])
def CrearHiloAction():
    hilo = Hilo()
    hilo.setTitulo(request.form.get("titulo"))
    hilo.setPropietario(Usuario.getUsuario(session['userid']))
    hilo.setFechaCreacion(date.today())
    hilo.setDescripcion(request.form.get("descripcion"))
    hilo.guardate()
    return redirect("/usuarioHilos")



@app.route('/crearPostAction', methods=['GET', 'POST'])
def CrearPostAction():
    post = Post()
    post.setFechaCreacion(date.today())
    post.setTitulo(request.form.get("titulo"))
    post.setCuerpo(None)
    post.setHilo(Hilo.getHilo(int(request.form.get("idhilo"))))
    post.guardate()
    return redirect("/postDeHilo?idhilo=" + request.form.get("idhilo"))

@app.route('/post')
def cargarPost():
    post = Post.getPost(int(request.args.get("idpost")))
    return render_template("/post.html", Post= post, usuario=Usuario.getUsuario(session['userid']), dueño=post.getDueño())

@app.route('/editarPost')
def editarPost():
    return render_template("/editarPost.html", Post=Post.getPost(int(request.args.get("idpost"))))

@app.route('/editarPostAction', methods=['GET', 'POST'])
def editarPostAction():

    post = Post.getPost(int(request.form.get("idpost")))
    if post.getDueño().id == Usuario.getUsuario(session["userid"]).id:
        post.setCuerpo(request.form.get("cuerpo"))
        post.setTitulo(request.form.get("titulo"))
        post.guardate()
    return redirect('/post?idpost=' + str(post.id))

if __name__ == '__main__':  # para actualizar automaticamente la pagina sin tener que cerrarla
    app.run(debug=True)  # para correr la pagina se puede hacer en este caso "python3 PruebaFlask.py" en la terminal
