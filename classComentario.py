from classUsuario import *
from classPost import *

class Comentario(object):
    id = None
    post = None
    usuario = None
    fecha = None
    cuerpo = None

    def setId(self, id):
        self.id = id

    def setPost(self, post):
        self.post = post

    def setUsuario(self, usuario):
        self.usuario = usuario

    def setFecha(self, fecha):
        self.fecha = fecha

    def setCuerpo(self, cuerpo):
        self.cuerpo = cuerpo

    def deserializar(self, dict):
        self.setId(dict["idcomentario"])
        self.setPost(Post.getPost(dict["post_idpost"]))
        self.setUsuario(Usuario.getUsuario(dict["usuario_idusuario"]))
        self.setFecha(dict["fecha"])
        self.setCuerpo(dict["cuerpo"])

    def insertate(self):
        cur = DB().run("INSERT INTO comentario VALUES (NULL, %i, %i, '%s', '%s')"
                       %(self.post.id, self.usuario.id, self.fecha, self.cuerpo))
        self.setId(cur.lastrowid)

    def actualizate(self):
        DB().run("UPDATE comentario SET post_idpost = %i, usuario_idusuario = %i, fecha = '%s', cuerpo = '%s' WHERE idcomentario = %i"
                 %(self.post.id, self.usuario.id, self.fecha, self.cuerpo, self.id))

    def eliminate(self):
        DB().run("DELETE FROM comentario WHERE idcomentario = %i" %self.id)

    @staticmethod
    def getComentario(id):
        comentario = Comentario()
        cur = DB().run("SELECT * FROM comentario WHERE idcomentario = %i" %id)
        dict = cur.fetchone()
        comentario.deserializar(dict)
        return comentario

    @staticmethod
    def getAllComentarios():
        cur = DB().run("SELECT * FROM comnetario")
        listaDict = cur.fetchall()
        listaComentarios = []
        for item in listaDict:
            listaComentarios.append(Comentario.getComentario(item["idcomentario"]))