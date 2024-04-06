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
import os
import requests
from flask import Flask, request, render_template, jsonify
from models import Favorite


api_key = 'JyXG87zvWmnQIa28tx4O3OBJ87mxXlrGr8kDnP9_JEo'

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

    @app.route('/favorites')
    @login_required
    def favorites():
        user_favorites = Favorite.query.filter_by(user_id=current_user.id).all()
        
        # Debugging: Log out some details of each favorite to verify their existence
        for favorite in user_favorites:
            print(f"Plant Name: {favorite.plant_name}, Image URL: {favorite.plant_image_url}")
        
        return render_template('favorites.html', favorites=user_favorites)
            
    @app.route('/search')
    def search():
        return render_template('search.html')


    @app.route('/api/search_plants', methods=['POST'])
    def api_search_plants():
        data = request.json  # Get JSON data from the request
        plant_name = data.get('plant_name')  # Access the plant_name field
        plant_data = fetch_plant_data(plant_name)
        if plant_data and 'data' in plant_data:
            # Transforming the response to include only necessary info
            simplified_data = [
                {
                    'common_name': plant.get('common_name'), 
                    'scientific_name': plant.get('scientific_name'), 
                    'image_url': plant.get('image_url')
                } for plant in plant_data['data']
            ]
            return jsonify(simplified_data)  # Return the simplified plant data
        return jsonify([])  # Return an empty list if no data is found

    def fetch_plant_data(plant_name):
        """Fetches data for a given plant name from the Trefle API."""
        api_url = f"https://trefle.io/api/v1/plants/search?token={api_key}&q={plant_name}"
        response = requests.get(api_url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
        
    @app.route('/update_favorites', methods=['POST'])
    @login_required
    def update_favorites():
        data = request.json
        plant_name = data.get('plant_name')
        bookmarked = data.get('bookmarked')
        plant_common_name = data.get('plant_common_name', '')
        plant_scientific_name = data.get('plant_scientific_name', '')
        plant_image_url = data.get('plant_image_url', '')
        plant_description = data.get('plant_description', '')
        # Assuming these additional fields are optional, provide default values
        duration = data.get('duration', 'N/A')
        edible = data.get('edible', False)
        vegetable = data.get('vegetable', False)
        edible_parts = data.get('edible_parts', 'N/A')
        synonyms = data.get('synonyms', 'None')

        favorite = Favorite.query.filter_by(user_id=current_user.id, plant_name=plant_name).first()

        if bookmarked and not favorite:
            new_favorite = Favorite(
                user_id=current_user.id,
                plant_name=plant_name,
                plant_common_name=plant_common_name,
                plant_scientific_name=plant_scientific_name,
                plant_image_url=plant_image_url,
                plant_description=plant_description,
                duration=duration,
                edible=edible,
                vegetable=vegetable,
                edible_parts=edible_parts,
                synonyms=synonyms
            )
            db.session.add(new_favorite)
            db.session.commit()
            return jsonify({'bookmarked': True})
        elif not bookmarked and favorite:
            db.session.delete(favorite)
            db.session.commit()
            return jsonify({'bookmarked': False})

        return jsonify({'error': 'Unknown error occurred'}), 500




    return app

# Outside the create_app function to ensure the app is created at import time
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)