# Imports
from flask_pymongo import PyMongo
from flask import Flask, render_template, url_for, request, session, redirect
from forms import MainForm

# Configuration de l'application Flask avec la base de données Mongo
app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'database_steam'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/database_steam'
app.config.update(SECRET_KEY='yoursecretkey')

mongo = PyMongo(app)


# Fonction pour récupérer tous les jeux de la base de données, triés alphabétiquement par leur titre
def get_all():
    search_get_all = list(mongo.db.collection_steam.find().sort([('Datetime', -1), ('Titre', 1)]))
    
    # Pop des éléments non désirés dans le html
    for i in range(len(search_get_all)):
        search_get_all[i].pop('_id')
        search_get_all[i].pop('Datetime')
    return search_get_all

# Fonction pour récupérer les jeux qui correspondent aux éléments donnés dans le formulaire
def search_games(form):
    title = form.title.data
    genre = form.genre.data
    dev = form.dev.data
    edit = form.edit.data
    date = form.date.data

    # Utilisation des expressions régulières pour donner de la souplesse à la recherche
    if(date == 'new'):
        search = list(mongo.db.collection_steam.find({'Titre': { '$regex': title, '$options':"i" }, 'Genre': { '$regex': genre, '$options':"i" }, 'Développeur': { '$regex': dev, '$options':"i" }, 'Éditeur': { '$regex': edit, '$options':"i" }}).sort([('Datetime', -1), ('Titre', 1)]))
    else:
        search = list(mongo.db.collection_steam.find({'Titre': { '$regex': title, '$options':"i" }, 'Genre': { '$regex': genre, '$options':"i" }, 'Développeur': { '$regex': dev, '$options':"i" }, 'Éditeur': { '$regex': edit, '$options':"i" }}).sort([('Datetime', 1), ('Titre', 1)]))
    
    # Pop des éléments non désirés dans le html
    for i in range(len(search)):
        search[i].pop("_id")
        search[i].pop('Datetime')
    return search



# Route principale de l'application Flask
@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' in session:
        mform_2 = MainForm()
        if mform_2.validate_on_submit() :
            return render_template('main.html', mform = mform_2, username = session['username'], search = search_games(mform_2))

        return render_template('main.html', mform = mform_2, username = session['username'], search=get_all())

    return render_template('index.html')

# Route d'inscription des utilisateurs
@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            users.insert({'name' : request.form['username'], 'password' : request.form['pass']})
            session['username'] = request.form['username']
            return redirect('/')
        
        return redirect('/error_register')

    return render_template('register.html')

# Route de connexion des utilisateurs
@app.route('/login',methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user :
        #mform = MainForm()
        if (request.form['pass'].encode('utf-8') == login_user['password'].encode('utf-8')):
            session['username'] = request.form['username']
            #return render_template('main.html', mform = mform, username = session['username'], search=get_all())
            return redirect('/')

    return redirect('/error_login')

# Route d'erreur d'inscription
@app.route('/error_register')
def error_register(): 
    return render_template('error_register.html')

# Route d'erreur de connexion
@app.route('/error_login')
def error_login(): 
    return render_template('error_login.html')

# Route de déconnexion de l'utilisateur
@app.route('/deco')
def deconnection():
    del session['username']
    return redirect('/')


