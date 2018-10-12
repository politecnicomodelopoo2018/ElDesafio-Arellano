from classDB import *
import hashlib
import smtplib



# HASH SHA256

class Usuario (object):
    id = None
    mail = None
    fechaCreacion = None
    nickName = None
    nombre = None
    apellido = None
    contraseña = None
    descripcion = None
    codigoCambio = None

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

    def setDescripcion(self, descripcion):
        self.descripcion = descripcion

    def setCodigoCambio(self, codigoCambio):
        self.codigoCambio = codigoCambio

    def deserializar(self, dict):
        self.setId(dict["idusuario"])
        self.setMail(dict["mail"])
        self.setFechaCreacion(dict["fechaCreacion"])
        self.setApellido(dict["apellido"])
        self.setNombre(dict["nombre"])
        self.setNickName(dict["nickName"])
        self.contraseña = (dict["contraseña"])
        self.setDescripcion(dict["descripcion"])
        self.setCodigoCambio(dict["codigoCambio"])

    def insertate(self):
        cur = DB().run("INSERT into usuario VALUES (NULL, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                       % (self.mail, self.fechaCreacion, self.nickName, self.nombre, self.apellido, self.contraseña, self.descripcion, self.codigoCambio))
        self.setId(cur.lastrowid)

    def actualizate(self):
        DB().run("UPDATE usuario SET mail = '%s', fechaCreacion = '%s', nickName = '%s', nombre = '%s', apellido = '%s', contraseña= '%s' , codigoCambio= '%s', descripcion = '%s' WHERE idusuario = %i"
                %(self.mail, self.fechaCreacion, self.nickName, self.nombre, self.apellido, self.contraseña, self.codigoCambio, self.descripcion, self.id))

    def guardate(self):
        if self.id is None:
            self.insertate()
        else:
            self.actualizate()

    def eliminate(self):
        DB().run("DELETE FROM usuario WHERE idusuario = %i" %self.id)

    def seguirUsuario(self, idUsuario):
        DB().run("INSERT into usuario_has_usuario VALUES (%i, %i)" %(idUsuario, self.id))

    def dejarDeSeguir(self, idUsuario):
        DB().run("DELETE from usuario_has_usuario WHERE idusuarioseguido = %i and idseguidor = %i" %(idUsuario, self.id))

    def verificarSiSigue(self, idUsuario):
        cur = DB().run("SELECT * from usuario_has_usuario WHERE idusuarioseguido = %i and idseguidor = %i" %(idUsuario, self.id))
        dict = cur.fetchone()
        if dict is None:
            return 0
        return 1

    def listaIdsSiguiendo(self):
        cur = DB().run("SELECT idusuarioseguido from usuario_has_usuario WHERE idseguidor = %i" %self.id)
        dict = cur.fetchall()
        listaIds = []
        for item in dict:
            listaIds.append(item["idusuarioseguido"])
        return listaIds

    def mailRecuperarContraseña(self):
        import uuid
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        self.setCodigoCambio(str(uuid.uuid4()))# generarCodigoCambio()
        self.guardate()
        # enviarMailCodigoCambio()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("arellano.ariel290@gmail.com", "54337641")

        msg = MIMEMultipart()
        msg['From'] = 'arellano.ariel290@gmail.com'
        msg['To'] = self.mail
        msg['Subject'] = 'Recuperación de Contraseña'
        part1 = MIMEText("El codigo de cambio es: <b>" + self.codigoCambio + "</b>", 'html')
        msg.attach(part1)

        server.sendmail("arellano.ariel290@gmail.com", self.mail, msg.as_string())
        server.quit()

    @staticmethod
    def getUsuario(id):
        usuario = Usuario()
        if id == 0:
            return
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

    # @staticmethod
    # def getHilosUsuario(id):
    #     cur = DB().run("SELECT * FROM hilo WHERE usuario_idusuario = %i" %id)
    #     listaDict = cur.fetchall()
    #     listaHilos = []
    #     for item in listaDict:
    #         listaHilos.append(Hilo.getHilo(item["idhilo"]))
    #     return listaHilos

    @staticmethod
    def getSeguidoresUsuario(id):
        cur = DB().run("SELECT idseguidor FROM usuario_has_usuario WHERE idusuarioseguido = %i" %id)
        listaDict = cur.fetchall()
        listaUsuarios = []
        for item in listaDict:
            listaUsuarios.append(Usuario.getUsuario(item["idseguidor"]))
        return listaUsuarios

    # @staticmethod
    # def getComentariosUsuario(id):
    #     cur = DB().run("SELECT * from comentario WHERE usuario_idusuario = %i" %id)
    #     listaDict = cur.fetchall()
    #     listaComentarios = []
    #     for item in listaDict:
    #         listaComentarios.append(Comentario.getComentario(item["idcomentario"]))
    #     return listaComentarios

    @staticmethod
    def todasLasIdUsuarios():
        cur = DB().run("SELECT idusuario FROM usuario")
        listaDict = cur.fetchall()
        listaIds = []
        for item in listaDict:
            listaIds.append(item["idusuario"])
        return listaIds
