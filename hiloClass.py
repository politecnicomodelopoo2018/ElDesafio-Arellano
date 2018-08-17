from usuarioClass import *

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
        self.fechaCreacion = dict["fechaCreacion"]
        self.titulo = dict["titulo"]
        self.descripcion = dict["descripcion"]
        self.propietario = Usuario.getUsuario(dict["usuario_idusuario"])

    def insertate(self):
        cur = DB().run("INSERT INTO hilo VALUES (NULL, %i, '%s', '%s', '%s')"
                       % (self.propietario.id, self.fechaCreacion, self.titulo, self.descripcion))
        self.setId(cur.lastrowid)
    def actualizate(self):
        DB().run("UPDATE hilo SET fechaCreacion = '%s', titulo = '%s', descripcion = '%s', usuario_idusuario = %i WHERE idhilo = %i"
                 % (self.fechaCreacion, self.titulo, self.descripcion,self.propietario.id, self.id))

    def eliminate(self):
        DB().run("DELETE FROM hilo WHERE idhilo = %i" %self.id)

