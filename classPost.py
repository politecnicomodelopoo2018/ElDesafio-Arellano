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
        cur = DB().run("INSERT INTO post VALES(NULL, %i, '%s', '%s', '%s')"
                       % (self.hilo.id, self.fechaCreacion, self.titulo, self.cuerpo))
        self.setId(cur.lastrowid)

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

    @staticmethod
    def getTagsPost(id):
        cur = DB().run("SELECT * FROM tag_has_post WHERE post_idpost = %i" %id)
        listaDict = cur.fetchall()
        listaTags = []
        for item in listaDict:
            listaTags.append(Tag.getTag(item["idtag"]))
        return listaTags


