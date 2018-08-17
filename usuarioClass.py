from DBClass import *
from hiloClass import *

class Usuario (object):
    id = None
    mail = None
    fechaCreacion = None
    nickName = None
    nombre = None
    apellido = None

    def setId(self, id):
        self.id = id

    def setMail(self, mail):
        self.mail = mail

    def setFechaCreacion(self, fechaCreacion):
        self.fechaCreacion = fechaCreacion

    def setNickName(self, nickName):
        self.nickName = nickName

    def setNombre(self, nombre):
        self.nombre = nombre

    def setApellido(self, apellido):
        self.apellido = apellido

    def deserializar(self, dict):
        self.setMail(dict["mail"])
        self.setFechaCreacion(dict["fechaCreacion"])
        self.setApellido(dict["apellido"])
        self.setNombre(dict["nombre"])
        self.setNickName(dict["nickName"])

    def insertate(self):
        cur = DB().run("INSERT into usuario VALUES (NULL, '%s', '%s', '%s', '%s', '%s')"
                       % (self.mail, self.fechaCreacion, self.nickName, self.nombre, self.apellido))
        self.setId(cur.lastrowid)

    def actualizate(self):
        DB().run("UPDATE usuario SET mail = '%s', fechaCreacion = '%s', nickName = '%s', nombre = '%s', apellido = '%s' WHERE id = %i"
                % (self.mail, self.fechaCreacion, self.nickName, self.nombre, self.apellido, self.id))

    def eliminate(self):
        DB().run("DELETE FROM usuario WHERE idusuario = %i" %self.id)

    @staticmethod
    def getUsuario(id):
        usuario = Usuario()
        cur = DB().run("SELECT * FROM usuario WHERE idusuario = %i" %id)
        dict = cur.fetchone()
        usuario.deserializar(dict)
        return usuario

    def getAllUsuarios(self):
        cur = DB().run("SELECT * FROM usuario")
        listaDict = cur.fetchall()
        listaUsuarios = []
        for item in listaDict:
            listaUsuarios.append(Usuario.getUsuario(item["idusuario"]))
        return listaUsuarios

    @staticmethod
    def getHilosUsuario(id):
        cur = DB().run("SELECT * FROM hilo WHERE usuario_idusuario = %i" %id)
        listaDict = cur.fetchall()
        listaHilos = []
        for item in listaDict:
            listaHilos.append(Hilo.getHilo(item["idhilo"]))
        return listaHilos