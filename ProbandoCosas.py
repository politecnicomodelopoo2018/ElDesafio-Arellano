from classUsuario import *
DB().setConnection('127.0.0.1', 'root', 'alumno', 'ElDesafio')



cur = DB().run("SELECT * FROM usuario WHERE mail = 'vos@vos.com'")
dict = cur.fetchone()
print("hi", dict["mail"])
print("cont", dict["contraseña"])
usuario = Usuario.getUsuarioDesdeMail("vos@vos.com")

