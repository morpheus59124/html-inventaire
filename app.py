from flask import *
import crud

app = Flask(__name__)
app.secret_key = '09c1a7ae6fe0c8355f2041414167e7aeb3bc1afc43be7361fa514f044a2ba4d9'

@app.route("/")
def index():
    if "user_mail" in session:
        if session["admin"] == True:
            return render_template('admin/index.html', title='Accueil')
        else:
            return render_template('user/index.html', title='Accueil')
    else:
        return redirect(url_for('login'))

#               #
#   REGISTER    #
#               #
@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    # Formulaire envoyé ?
    if request.method == 'POST':
        user_firstname = request.form['user_firstname']
        user_surname = request.form['user_surname']
        user_mail = request.form['user_mail']
        user_password = request.form['user_password']
        # Deja inscrit ?
        if crud.is_register(user_mail):
            error = 'Adresse email déjà utilisée ! '
        else:
            crud.create_user(False, user_surname, user_firstname, user_mail, user_password)
            return redirect(url_for('index'))
    # Deja connecter ?
    if len(session) > 0:
        return redirect(url_for('index'))
    return render_template('register.html', title='Inscription', error = error)


#               #
#     LOGIN     #
#               #
@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    # Formulaire envoyé ?
    if request.method == 'POST':
        user_mail = request.form['user_mail']
        user_password = request.form['user_password']
        # Utilisateur inscrit ?
        if crud.verify_user(user_mail, user_password) != None:
            user_infos = crud.get_info_user(user_mail)
            session['user_mail'] = user_mail
            session['logged'] = True
            if user_infos[1] == 1:
                session['admin'] = True
            else:
                session['admin'] = False
            return redirect(url_for('index'))
        else:
            error = 'Adresse mail / Mot de passe incorrect ! '
    # Deja connecter ?
    if len(session) > 0:
        return redirect(url_for('index'))
    return render_template('login.html', title='Connexion', error = error)


#               #
#    LOGOUT     #
#               #
@app.route("/logout")
def logout():
    if "user_mail" in session:
        session.clear()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


#               #
#  ADMIN USER   #
#               #
@app.route("/admin/users")
def admin_users():
    if session["admin"] == True:
        return render_template('admin/users.html')
    else:
        return redirect(url_for(''))