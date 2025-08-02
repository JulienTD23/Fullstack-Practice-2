# makes the website folder a python package - whatever is in this file is ran automatically when website is imported
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = path.join(path.dirname(__file__), 'database.db')

# creating a flask application
def create_app():
    app = Flask(__name__) # name of the file
    app.config['SECRET_KEY'] = 'hasd8dsfsdoifj' #encrypts cookies & session data - secret key
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    #register blueprints
    from .views import views 
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    #create the database
    from .models import User, Note
    
    with app.app_context():
        create_database()
        
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    #tell flask what user we're looking for - login manager for flask 
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database():
    # check if path to database exists - if not, don't override it
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print('Created Database.') 