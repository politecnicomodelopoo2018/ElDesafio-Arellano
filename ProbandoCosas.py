# from classUsuario import *
# DB().setConnection('127.0.0.1', 'root', 'alumno', 'ElDesafio')
# from classHilo import *
#
#
# # cur = DB().run("SELECT * FROM usuario WHERE mail = 'vos@vos.com'")
# # dict = cur.fetchone()
# # print("hi", dict["mail"])
# # print("cont", dict["contraseña"])
# # usuario = Usuario.getUsuarioDesdeMail("vos@vos.com")
#
#
#
# dict = cur.fetchone()
# print(dict)

# l = [1,5,2]
# print(placeholders)




import smtplib



server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("arellano.ariel290@gmail.com", "54337641")

msg = "Esta prueba"
server.sendmail("arellano.ariel290@gmail.com", "krollarellano@gmail.com", msg)
server.quit()
