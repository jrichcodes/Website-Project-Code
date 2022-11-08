from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdajah'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Trip

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
    
def create_database(app): #checking if database exists if not it creates a new database
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def clear_database(app):
    
    from .models import tripTypes, menuTypes

    if not path.exists('website/' + DB_NAME):
        print('No database to clear')
    
    with app.app_context():
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()

        #adding trip types and menu types back to database
        types = [
            tripTypes(type = "backpacking"),
            tripTypes(type = "climbing"),
            tripTypes(type = "kayaking"),
            tripTypes(type = "biking"),
            menuTypes(type = "breakfast"),
            menuTypes(type = "lunch"),
            menuTypes(type = "dinner"),
            menuTypes(type = "snack")
        ]

        db.session.add_all(types)
        db.session.commit()

    print("Database cleared!")