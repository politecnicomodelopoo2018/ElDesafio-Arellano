from classDB import *
import hashlib
from classComentario import *

# HASH SHA256

class Usuario (object):
    id = None
    mail = None
    fechaCreacion = None
    nickName = None
    nombre = None
    apellido = None
    contraseña = None

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

    def setContraseña(self, contraseña):
        self.contraseña = hashlib.sha256((contraseña).encode('utf-8')).hexdigest()

    def deserializar(self, dict):
        self.setId(dict["idusuario"])
        self.setMail(dict["mail"])
        self.setFechaCreacion(dict["fechaCreacion"])
        self.setApellido(dict["apellido"])
        self.setNombre(dict["nombre"])
        self.setNickName(dict["nickName"])
        self.contraseña = (dict["contraseña"])

    def insertate(self):
        cur = DB().run("INSERT into usuario VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s')"
                       % (self.mail, self.fechaCreacion, self.nickName, self.nombre, self.apellido, self.contraseña))
        self.setId(cur.lastrowid)

    def actualizate(self):
        DB().run("UPDATE usuario SET mail = '%s', fechaCreacion = '%s', nickName = '%s', nombre = '%s', apellido = '%s' contraseña= '%s' WHERE id = %i"
                % (self.mail, self.fechaCreacion, self.nickName, self.nombre, self.apellido, self.contraseña, self.id))

    def guardate(self):
        if self.id is None:
            self.insertate()
        else:
            self.actualizate()

    def eliminate(self):
        DB().run("DELETE FROM usuario WHERE idusuario = %i" %self.id)

    @staticmethod
    def getUsuario(id):
        usuario = Usuario()
        cur = DB().run("SELECT * FROM usuario WHERE idusuario = %i" %id)
        dict = cur.fetchone()
        usuario.deserializar(dict)
        return usuario

    @staticmethod
    def getUsuarioDesdeMail(mail):
        usuario = Usuario()
        cur = DB().run("SELECT * FROM usuario WHERE mail = '%s'" % mail)
        dict = cur.fetchone()
        usuario.deserializar(dict)
        return usuario

    @staticmethod
    def getAllUsuarios():
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

    @staticmethod
    def getSeguidoresUsuario(id):
        cur = DB().run("SELECT idseguidor FROM usuario_has_usuario WHERE idusuarioseguido = %i" %id)
        listaDict = cur.fetchall()
        listaUsuarios = []
        for item in listaDict:
            listaUsuarios.append(Usuario.getUsuario(item["idseguidor"]))
        return listaUsuarios

    @staticmethod
    def getComentariosUsuario(id):
        cur = DB().run("SELECT * from comentario WHERE usuario_idusuario = %i" %id)
        listaDict = cur.fetchall()
        listaComentarios = []
        for item in listaDict:
            listaComentarios.append(Comentario.getComentario(item["idcomentario"]))
        return listaComentarios