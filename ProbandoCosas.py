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


if 'userid' in session:
    usuario = Usuario.getUsuario(session['userid'])



@app.route('/logOut')
def logout():
   session.pop('userid', None)
   return redirect("/")



@app.route('/loginAction', methods=['GET', 'POST'])
def LoginAction():
    usuario = Usuario.getUsuarioDesdeMail(request.form.get("mail"))
    if hashlib.sha256((request.form.get("contraseña")).encode('utf-8')).hexdigest() == usuario.contraseña:
        session['userid'] = usuario.id
    return redirect("/")




import smtplib



server = smtplib.SMTP('smtp.gmail.com', 587)


server.starttls()
server.login("arellano.ariel290@gmail.com", "54337641")
msg = "Esta prueba" + "jaja"
server.sendmail("arellano.ariel290@gmail.com", "krollarellano@gmail.com", msg)
server.quit()
