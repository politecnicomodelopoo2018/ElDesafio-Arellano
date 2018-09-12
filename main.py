
from flask import *
from datetime import date
from classComentario import *
DB().setConnection('127.0.0.1', 'root', 'alumno', 'ElDesafio')

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def Index():
    if 'userid' in session:
        return redirect("/homeUsuario?filtro=predeterminado")
    return render_template("/paginaPrincipal.html")

@app.route('/homeUsuario')
def homeUsuario():
    listaIds = []
    usuario = Usuario.getUsuario(session['userid'])
    if request.args.get("filtro") == "predeterminado":
        listaIds=Usuario.todasLasIdUsuarios()
        print(listaIds)
    elif request.args.get("filtro") == "siguiendo":
        listaIds=usuario.listaIdsSiguiendo()
        print(listaIds)
    print(listaIds)
    return render_template("/homeUsuario.html", usuario=usuario, listaPosts=Post.postsDeUsuarios(listaIds))

@app.route('/todosLosPosts')
def todosLosPosts():
    return render_template("/todosLosPosts.html", usuario=Usuario.getUsuario(session['userid']), listaPosts=Post.getAllPosts())

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
    return render_template("/usuarioHilos.html", usuario=Usuario.getUsuario(int(request.args.get("idusuario"))), ListaHilos=Hilo.hilosParaUsuario(session['userid']))


@app.route('/crearHilo')
def CrearHilo():
    return render_template("/crearHilo.html", usuario=Usuario.getUsuario(session['userid']))


@app.route('/postDeHilo')
def PostsDeHilo():
    hilo = Hilo.getHilo(int(request.args.get("idhilo")))
    return render_template("/postDeHilo.html", usuario=Usuario.getUsuario(session['userid']), ListaPosts=Post.postsParaHilo(hilo.id), Hilo=hilo)


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
    usuario = Usuario.getUsuario(session['userid'])
    post = Post.getPost(int(request.args.get("idpost")))
    for item in Comentario.getComentariosParaPost(post.id):
        print(item.cuerpo)
    return render_template("/post.html", Post=post, usuario=usuario, dueño=post.getDueño(), listaComentarios=Comentario.getComentariosParaPost(post.id), estadoLike=post.verificarLike(usuario), cantLikes=post.cantLikes())

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

@app.route('/comentar', methods=['GET', 'POST'])
def comentar():
    comentario = Comentario()
    comentario.setFecha(date.today())
    comentario.setCuerpo(request.form.get('cuerpo'))
    comentario.setUsuario(Usuario.getUsuario(session['userid']))
    comentario.setPost(Post.getPost(int(request.form.get("idpost"))))
    comentario.guardate()
    return redirect('/post?idpost=' + request.form.get("idpost"))

@app.route('/borrarComentario')
def borrarComentario():
    comentario = Comentario.getComentario(int(request.args.get("idcomentario")))
    if comentario.usuario.id == session["userid"] or (comentario.post.getDueño()).id == session["userid"]:
        comentario.eliminate()
    return redirect('/post?idpost=' + request.args.get("idpost"))

@app.route('/usuarioPerfil')
def usuarioPerfil():
    usuario = Usuario.getUsuario(int(request.args.get("idusuario")))
    sessionUser = Usuario.getUsuario(int(session["userid"]))
    return render_template('/usuarioPerfil.html', usuario=usuario, listaHilos=Hilo.hilosParaUsuario(usuario.id), estadoDeSeguir = sessionUser.verificarSiSigue(int(request.args.get("idusuario"))))

@app.route('/editarPerfil')
def editarPerfil():
    return render_template('editarPerfil.html', usuario=Usuario.getUsuario(session["userid"]))

@app.route('/editarPerfilAction', methods=['GET', 'POST'])
def editarPerfilAction():
    usuario = Usuario.getUsuario(session["userid"])
    usuario.setDescripcion(request.form.get("descripcion"))
    usuario.setNickName(request.form.get("nickName"))
    usuario.setMail(request.form.get("mail"))
    usuario.guardate()
    return redirect("/usuarioPerfil?idusuario=" + str(usuario.id))

@app.route('/seguir')
def seguir():
    usuario = Usuario.getUsuario(session["userid"])
    if not usuario.verificarSiSigue(int(request.args.get("idusuario"))):
        usuario.seguirUsuario(int(request.args.get("idusuario")))
    return redirect("/usuarioPerfil?idusuario=" + str(request.args.get("idusuario")))

@app.route('/dejarDeSeguir')
def dejarDeSeguir():
    usuario = Usuario.getUsuario(session["userid"])
    if usuario.verificarSiSigue(int(request.args.get("idusuario"))):
        usuario.dejarDeSeguir(int(request.args.get("idusuario")))
    return redirect("/usuarioPerfil?idusuario=" + str(request.args.get("idusuario")))

@app.route('/arrivoto')
def arrivoto():
    post = Post.getPost(int(request.args.get("idpost")))
    usuario = Usuario.getUsuario(session["userid"])
    if not post.verificarLike(usuario):
        post.getLiked(usuario)
    return redirect("/post?idpost=" + str(post.id))


@app.route('/desarrivoto')
def desarrivoto():
    post = Post.getPost(int(request.args.get("idpost")))
    usuario = Usuario.getUsuario(session["userid"])
    if post.verificarLike(usuario):
        post.getUnliked(usuario)
    return redirect("/post?idpost=" + str(post.id))


if __name__ == '__main__':  # para actualizar automaticamente la pagina sin tener que cerrarla
    app.run(debug=True)  # para correr la pagina se puede hacer en este caso "python3 PruebaFlask.py" en la terminal
