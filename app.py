from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from forms import RegistrationForm
from flask_login import login_user
from forms import LoginForm
from flask_login import logout_user
from forms import RegistrationForm 
from models import User
from extensions import db, migrate, login_manager

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plantexplorer.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'urmom'

    # Initialize extensions with the app instance here
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        # Directly use User model within the function to avoid circular imports
        return User.query.get(int(user_id))

    # Define all your routes within create_app to ensure they are part of the application context
    @app.route('/')
    def home():
        return render_template('index.html', hide_nav=False)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            existing_user = User.query.filter_by(username=form.username.data).first()
            if existing_user:
                flash('Username already taken. Please choose a different one.', 'error')
                return render_template('register.html', form=form, hide_nav=True)
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Congratulations, you are now a registered user!', 'info')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form, hide_nav=True, centered=True)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('home'))
            flash('Invalid username or password')
        return render_template('login.html', title='Sign In', form=form, centered=True)

    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/search')
    def search():
        # Your search functionality
        return render_template('search.html')

    @app.route('/favorites')
    @login_required
    def favorites():
        # Fetch the user's favorite plants logic here
        sample_favorites = []  # This is a placeholder
        return render_template('favorites.html', favorites=sample_favorites)

    return app

# Outside the create_app function to ensure the app is created at import time
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)