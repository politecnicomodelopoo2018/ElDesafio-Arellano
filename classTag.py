from classPost import *

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

    @staticmethod
    def getTag(id):
        tag = Tag()
        cur = DB().run("SELECT * FROM tag WHERE idtag = %i" %id)
        dict = cur.fetchone()
        tag.getTag(dict["idtag"])
        return tag

    @staticmethod
    def getAllTag():
        cur = DB().run("SELECT * FROM tag")
        listaDict = cur.fetchall()
        listaTags = []
        for item in listaDict:
            listaTags.append(Tag.getTag(item["idtag"]))
        return listaTags

    @staticmethod
    def getPostsTag(id):
        cur = DB().run("SELECT * FROM tag_has_post WHERE tag_idtag = %i" %id)
        listaDict = cur.fetchall()
        listaPosts = []
        for item in listaDict:
            listaPosts.append(Post.getPost(item["idpost"]))
        return listaPosts

