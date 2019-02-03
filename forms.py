# Imports
from flask_wtf import FlaskForm
from wtforms import TextField, SelectField, SubmitField
#from wtforms.validators import DataRequired

# Création du formulaire de recherche de jeu
class MainForm(FlaskForm):
    title = TextField('Titre')
    genre = TextField('Genre')
    dev = TextField('Développeur')
    edit = TextField('Éditeur')
    date = SelectField(u'Date', 
                choices=[('new', 'Récents'), ('last', 'Anciens'), 
                        ], 
                id = 'selectmenu_chrono',
                default = ('new', 'Récents'))
    
    submit = SubmitField('Rechercher')