from classHilo import *

class Post(object):
    id = None
    hilo = None
    fechaCreacion = None
    titulo = None
    cuerpo = None

    def setId(self, id):
        self.id = id

    def setHilo(self, hilo):
        self.hilo = hilo

    def setFechaCreacion(self, fechaCreacion):
        self.fechaCreacion = fechaCreacion

    def setTitulo(self, titulo):
        self.titulo = titulo

    def setCuerpo(self, cuerpo):
        self.cuerpo = cuerpo

    def deserializar(self, dict):
        self.setId(dict["idpost"])
        self.setTitulo(dict["titulo"])
        self.setFechaCreacion(dict["fechaCreacion"])
        self.setCuerpo(dict["cuerpo"])
        self.setHilo(Hilo.getHilo(dict["hilo_idhilo"]))

    def insertate(self):
        cur = DB().run("INSERT INTO post VALUES(NULL, %i, '%s', '%s', '%s')"
                       % (self.hilo.id, self.fechaCreacion, self.titulo, self.cuerpo))
        self.setId(cur.lastrowid)

    def actualizate(self):
        DB().run("UPDATE post SET hilo_idhilo = %i, fechaCreacion = '%s', titulo = '%s', cuerpo = '%s' WHERE idpost = %i"
                 % (self.hilo.id, self.fechaCreacion, self.titulo, self.cuerpo, self.id))

    def guardate(self):
        if self.id == None:
            self.insertate()
        else:
            self.actualizate()

    def eliminate(self):
        DB().run("DELETE FROM post WHERE idpost = %i" % self.id)

    def getDueño(self):
        cur = DB().run("SELECT GetIdDueñoDePost(%i) as idusuario" %self.id)
        dict = cur.fetchone()
        return Usuario.getUsuario(dict["idusuario"])

    def getLiked(self, Usuario):
        DB().run("INSERT INTO arrivoto VALUES(%i, %i)" %(self.id, Usuario.id))

    def getUnliked(self, Usuario):
        DB().run("DELETE FROM arrivoto WHERE post_idpost = %i and usuario_idusuario = %i" %(self.id, Usuario.id))

    def verificarLike(self, Usuario):
        cur = DB().run("SELECT * FROM arrivoto WHERE post_idpost = %i and usuario_idusuario = %i" %(self.id, Usuario.id))
        dict = cur.fetchone()
        if dict is None:
            return 0
        return 1

    def cantLikes(self):
        cur = DB().run("SELECT count(*) as numero FROM arrivoto WHERE post_idpost = %i" %self.id)
        dict = cur.fetchone()
        return dict["numero"]

    @staticmethod
    def getPost(id):
        post = Post()
        cur = DB().run("SELECT * FROM post WHERE idpost = %i" %id)
        dict = cur.fetchone()
        post.deserializar(dict)
        return post

    @staticmethod
    def getAllPosts():
        cur = DB().run("SELECT * FROM post")
        listaDict = cur.fetchall()
        listaPosts = []
        for item in listaDict:
            listaPosts.append(Post.getPost(item["idpost"]))
        return listaPosts

    # @staticmethod
    # def getTagsPost(id):
    #     cur = DB().run("SELECT * FROM tag_has_post WHERE post_idpost = %i" %id)
    #     listaDict = cur.fetchall()
    #     listaTags = []
    #     for item in listaDict:
    #         listaTags.append(Tag.getTag(item["idtag"]))
    #     return listaTags

    @staticmethod
    def postsParaHilo(id):
        cur = DB().run("SELECT * FROM post WHERE hilo_idhilo=%i" %id)
        listaDict = cur.fetchall()
        listaPosts = []
        for item in listaDict:
            listaPosts.append(Post.getPost(item["idpost"]))
        return listaPosts

    @staticmethod
    def postsDeUsuarios(lista):
        listaPosts = []
        for item in lista:
            print("temi " + str(item))
            cur = DB().run("SELECT * FROM post WHERE hilo_idhilo IN (SELECT idhilo FROM hilo WHERE usuario_idusuario = %i)" %item)
            for post in cur:
                listaPosts.append(Post.getPost(post["idpost"]))
        return listaPosts

    @staticmethod
    def postsPorFiltro(campo, texto):
        listaPosts = []
        cur = DB().run("SELECT * FROM post WHERE {0} LIKE '{1}%'".format(campo, texto))
        for post in cur:
            listaPosts.append(Post.getPost(post["idpost"]))
        return listaPosts