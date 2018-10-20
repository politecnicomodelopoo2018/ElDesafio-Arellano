
from flask import *
from datetime import date
from classComentario import *


DB().setConnection('127.0.0.1', 'root', 'alumno', 'ElDesafio')

app = Flask(__name__, static_url_path='/static')
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

anonimo = Usuario()
anonimo.setNickName("Anonimo")
anonimo.setId(-1)

usuarioSession = Usuario()

@app.route('/')
def Index():
    return redirect("/homeUsuario?filtro=predeterminado")


@app.route('/probando')
def probando():
    return render_template("probando.html")

# Aca hay que arreglar lo del offset
@app.route('/homeUsuario', methods=['GET', 'POST'])
def homeUsuario():
    buscarPor = None
    busqueda = None

    if 'offset' in request.args and 'move' in request.args:
        offset = int(request.args.get('offset')) + int(request.args.get('move'))
    else:
        offset = 0
    if offset < 0:
        offset=0
    listaIds = []
    listaPosts = []
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    fil = request.args.get("filtro")

    # fixeado aca
    if request.args.get("filtro") == "predeterminado":
        listaIds=Usuario.todasLasIdUsuarios()
        idsParaSQL = ', '.join(str(e) for e in listaIds)
        if offset > Post.cantPosts(idsParaSQL):
            offset = offset-2
        listaPosts = Post.postsDeUsuarios(idsParaSQL, offset)
    # fixeado aca
    elif request.args.get("filtro") == "siguiendo":
        listaIds=usuario.listaIdsSiguiendo()
        idsParaSQL = ', '.join(str(e) for e in listaIds)
        if offset > Post.cantPosts(idsParaSQL):
            offset = offset-2
        listaPosts = Post.postsDeUsuarios(idsParaSQL, offset)

    elif request.args.get("filtro") == "buscar":
        if int(request.args.get("X")) == 0:
            buscarPor = request.form.get("buscarPor")
            busqueda = request.form.get("busqueda")
            if offset > Post.cantPostPorFiltro(buscarPor, busqueda):
                offset=offset-2
            listaPosts = Post.postsPorFiltro(buscarPor, busqueda, offset)
        elif int(request.args.get("X")) == 1:
            buscarPor = request.args.get("buscarPor")
            busqueda = request.args.get("busqueda")
            if offset > Post.cantPostPorFiltro(buscarPor, busqueda):
                offset=offset-2
            listaPosts = Post.postsPorFiltro(buscarPor, busqueda, offset)
    return render_template("/homeUsuario.html", usuario=usuario, listaPosts=listaPosts, offset=offset, filtro=fil, buscarPor=buscarPor, busqueda=busqueda)

@app.route('/todosLosPosts')
def todosLosPosts():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    return render_template("/todosLosPosts.html", usuario=usuario, listaPosts=Post.getAllPosts())

@app.route('/logIn')
def Login():
    #Parece que el problema era que no estaba como int
    err = int(request.args.get("err"))
    if 'err' in request.args:
        return render_template("/logIn.html", err=err)
    if 'userid' in session:
        return redirect("/")
    return render_template("/logIn.html", err=0)


@app.route('/loginAction', methods=['GET', 'POST'])
def LoginAction():
    cur = DB().run("SELECT mail FROM usuario WHERE mail = '{0}'".format(request.form.get("mail")))
    dict = cur.fetchone()
    if dict is None:
        return redirect("/logIn?err=1")
    usuario = Usuario.getUsuarioDesdeMail(request.form.get("mail"))
    if hashlib.sha256((request.form.get("contraseña")).encode('utf-8')).hexdigest() == usuario.contraseña:
        session['userid'] = usuario.id
    else:
        return redirect("/logIn?err=2")
    return redirect("/")


@app.route('/signUp')
def signUp():
    return render_template("signUp.html")


@app.route('/registrarUsuario', methods=['GET', 'POST'])
def signUpAction():
    usuario = Usuario()
    usuario.setNombre(request.form.get("nombre"))
    usuario.setMail(request.form.get("mail"))
    usuario.setFechaCreacion(date.today())
    usuario.setNickName(request.form.get("nickName"))
    usuario.setApellido(request.form.get("apellido"))
    usuario.setContraseña(request.form.get("contraseña"))
    if request.form.get("mail") == "" or request.form.get("nickName") == "" or len(request.form.get("contraseña")) < 4:
        return redirect("/")
    usuario.guardate()
    return redirect("/")


@app.route('/usuarioHilos')
def UsuarioHilos():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    return render_template("/usuarioHilos.html", usuario=usuario, ListaHilos=Hilo.hilosParaUsuario(int(request.args.get("idusuario"))))


@app.route('/crearHilo')
def CrearHilo():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    return render_template("/crearHilo.html", usuario=usuario)


@app.route('/postDeHilo')
def PostsDeHilo():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    hilo = Hilo.getHilo(int(request.args.get("idhilo")))
    return render_template("/postDeHilo.html", usuario=usuario, ListaPosts=Post.postsParaHilo(hilo.id), Hilo=hilo)


@app.route('/crearPost')
def CrearPost():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    return render_template("/crearPost.html", listaHilos=Hilo.hilosParaUsuario(usuario.id), usuario=usuario)








@app.route('/logOut')
def logout():
   session.pop('userid', None)
   return redirect("/")


@app.route('/crearHiloAction', methods=['GET', 'POST'])
def CrearHiloAction():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    if usuario.id == -1:
        return redirect("/logIn")
    hilo = Hilo()
    hilo.setTitulo(request.form.get("titulo"))
    hilo.setPropietario(usuario)
    hilo.setFechaCreacion(date.today())
    hilo.setDescripcion(request.form.get("descripcion"))
    hilo.guardate()
    return redirect("/crearPost")


@app.route('/usuarioPerfil')
def usuarioPerfil():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    usuarioPerfil = Usuario.getUsuario(int(request.args.get("idusuario")))
    sessionUser = usuario
    return render_template('/usuarioPerfil.html', usuarioPerfil=usuarioPerfil, usuario=sessionUser, listaHilos=Hilo.hilosParaUsuario(usuarioPerfil.id), estadoDeSeguir = sessionUser.verificarSiSigue(int(request.args.get("idusuario"))))


@app.route('/crearPostAction', methods=['GET', 'POST'])
def CrearPostAction():
    post = Post()
    post.setFechaCreacion(date.today())
    post.setTitulo(request.form.get("titulo"))
    post.setCuerpo(None)
    post.setHilo(Hilo.getHilo(int(request.form.get("idhilo"))))
    post.guardate()
    return redirect("/postDeHilo?idhilo=" + request.form.get("idhilo"))


@app.route('/cambiarContraseña')
def cambiarContraseña():

    return render_template('cambiarContraseña.html')


@app.route('/cambiarContraseñaAction', methods=['GET', 'POST'])
def cambiarContraseñaAction():
    usuario = Usuario.getUsuarioDesdeMail(request.form.get("mail"))
    usuario.mailRecuperarContraseña()
    return redirect("/cambiarContraseña2?usuarioId=" + str(usuario.id))


@app.route('/cambiarContraseña2')
def cambiarContraseña2():
    usuario = Usuario.getUsuario(int(request.args.get("usuarioId")))
    return render_template('cambiarContraseña2.html', usuario=usuario)


@app.route('/cambiarContraseña2Action', methods=['GET', 'POST'])
def cambiarContraseña2Action():
    usuario = Usuario.getUsuario(int(request.args.get("usuarioId")))
    if usuario.codigoCambio == request.form.get("codigo"):
        return redirect("/cambiarContraseña3?usuarioId=" + str(usuario.id))
    return redirect("/")


@app.route('/cambiarContraseña3')
def cambiarContraseña3():
    usuario = Usuario.getUsuario(int(request.args.get("usuarioId")))
    return render_template('cambiarContraseña3.html', usuario=usuario)


@app.route('/cambiarContraseña3Action', methods=['GET', 'POST'])
def cambiarContraseña3Action():
    usuario = Usuario.getUsuario(int(request.args.get("usuarioId")))
    usuario.setContraseña(request.form.get("contraseña"))
    usuario.guardate()
    return redirect('/')









@app.route('/post')
def cargarPost():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
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
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    if usuario.id == -1:
        return redirect("/logIn")
    comentario = Comentario()
    comentario.setFecha(date.today())
    comentario.setCuerpo(request.form.get('cuerpo'))
    comentario.setUsuario(usuario)
    comentario.setPost(Post.getPost(int(request.form.get("idpost"))))
    comentario.guardate()
    return redirect('/post?idpost=' + request.form.get("idpost"))


@app.route('/borrarComentario')
def borrarComentario():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    if usuario.id == -1:
        return redirect("/logIn")
    comentario = Comentario.getComentario(int(request.args.get("idcomentario")))
    if comentario.usuario.id == session["userid"] or (comentario.post.getDueño()).id == session["userid"]:
        comentario.eliminate()
    return redirect('/post?idpost=' + request.args.get("idpost"))


@app.route('/editarPerfil')
def editarPerfil():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    return render_template('editarPerfil.html', usuario=usuario)


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
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    if usuario.id == -1:
        return redirect("/logIn")
    if usuario.id == int(request.args.get("idusuario")):
        return redirect("/usuarioPerfil?idusuario=" + str(request.args.get("idusuario")))
    if not usuario.verificarSiSigue(int(request.args.get("idusuario"))):
        usuario.seguirUsuario(int(request.args.get("idusuario")))
    return redirect("/usuarioPerfil?idusuario=" + str(request.args.get("idusuario")))


@app.route('/dejarDeSeguir')
def dejarDeSeguir():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    if usuario.id == -1:
        return redirect("/logIn")
    if usuario.verificarSiSigue(int(request.args.get("idusuario"))):
        usuario.dejarDeSeguir(int(request.args.get("idusuario")))
    return redirect("/usuarioPerfil?idusuario=" + str(request.args.get("idusuario")))


@app.route('/arrivoto')
def arrivoto():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    if usuario.id == -1:
        return redirect("/logIn")
    post = Post.getPost(int(request.args.get("idpost")))

    if not post.verificarLike(usuario):
        post.getLiked(usuario)
    return redirect("/post?idpost=" + str(post.id))


@app.route('/desarrivoto')
def desarrivoto():
    if 'userid' in session:
        usuario = Usuario.getUsuario(session['userid'])
    else:
        usuario = anonimo
    if usuario.id == -1:
        return redirect("/logIn")
    post = Post.getPost(int(request.args.get("idpost")))
    if post.verificarLike(usuario):
        post.getUnliked(usuario)
    return redirect("/post?idpost=" + str(post.id))


if __name__ == '__main__':  # para actualizar automaticamente la pagina sin tener que cerrarla
    app.run(debug=True)  # para correr la pagina se puede hacer en este caso "python3 PruebaFlask.py" en la terminal
