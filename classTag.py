from classDB import *

class Tag(object):
    id = None
    nombre = None

    def setId(self, id):
        self.id = id

    def setNombre(self, nombre):
        self.nombre = nombre

    def deserializar(self, dict):
        self.setId(dict["idtag"])
        self.setNombre(dict["nombre"])

    def insertate(self):
        cur = DB().run("INSERT INTO tag VALUES(NULL, '%s')" %self.nombre)
        self.setId(cur.lastrowid)

    def actualizate(self):
        DB().run("UPADTE tag SET nombre = '%s'" %self.nombre)

    def eliminate(self):
        DB().run("DELETE FROM tag WHERE idtag = %i" %self.id)



