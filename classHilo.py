from classDB import *
from classUsuario import *

class Hilo(object):
    id = None
    fechaCreacion = None
    titulo = None
    descripcion = None
    propietario = None

    def setId(self, id):
        self.id = id

    def setFechaCreacion(self, fechaCreacion):
        self.fechaCreacion = fechaCreacion

    def setTitulo(self, titulo):
        self.titulo = titulo

    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def setPropietario(self, propietario):
        self.propietario = propietario

    def deserializar(self, dict):
        self.setId(dict["idhilo"])
        self.setFechaCreacion(dict["fechaCreacion"])
        self.setTitulo(dict["titulo"])
        self.setDescripcion(dict["descripcion"])
        self.setPropietario(Usuario.getUsuario(dict["usuario_idusuario"]))


    def insertate(self):
        cur = DB().run("INSERT INTO hilo VALUES (NULL, %i, '%s', '%s', '%s')"
                       % (self.propietario.id, self.fechaCreacion, self.titulo, self.descripcion))
        self.setId(cur.lastrowid)

    def actualizate(self):
        DB().run("UPDATE hilo SET fechaCreacion = '%s', titulo = '%s', descripcion = '%s', usuario_idusuario = %i WHERE idhilo = %i"
                 % (self.fechaCreacion, self.titulo, self.descripcion,self.propietario.id, self.id))

    def guardate(self):
        if self.id is None:
            self.insertate()
        else:
            self.actualizate()

    def eliminate(self):
        DB().run("DELETE FROM hilo WHERE idhilo = %i" %self.id)

    @staticmethod
    def getHilo(id):
        hilo = Hilo()
        cur = DB().run("SELECT * FROM hilo WHERE idhilo = %i" %id)
        dict = cur.fetchone()
        hilo.deserializar(dict)
        return hilo

    @staticmethod
    def getAllHilos():
        cur = DB().run("SELECT * FROM hilo")
        listaDict = cur.fetchall()
        listaHilos = []
        for item in listaDict:
            listaHilos.append(Hilo.getHilo(item["idhilo"]))
        return listaHilos

    # @staticmethod
    # def getPostsHilo(id):
    #     cur = DB().run("SELECT * FROM post WHERE hilo_idhilo = %i" %id)
    #     listaDict = cur.fetchall()
    #     listaPosts = []
    #     for item in listaDict:
    #         listaPosts.append(Post.getPost(item["idpost"]))
    #     return listaPosts

    @staticmethod
    def hilosParaUsuario(idusuario):
        cur = DB().run("SELECT * FROM hilo WHERE usuario_idusuario = %i" % idusuario)
        listaDict = cur.fetchall()
        listaHilos = []
        for item in listaDict:
            listaHilos.append(Hilo.getHilo(item["idhilo"]))
        return listaHilos
