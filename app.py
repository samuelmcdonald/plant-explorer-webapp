from concurrent.futures import ThreadPoolExecutor
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
from flask import request, jsonify
from models import Bookmark
from extensions import db


api_key = 'sk-stgs65f4ded3c05e34749'

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
    @login_required
    def home():
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        return render_template('index.html', username=current_user.username, hide_nav=False)

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
        favorites = Bookmark.query.filter_by(user_id=current_user.id).all()
        return render_template('favorites.html', favorites=favorites)
            
    @app.route('/search')
    @login_required
    def search():
        return render_template('search.html')


    @app.route('/api/search', methods=['GET'])
    @login_required
    def api_search():
        plant_name = request.args.get('q', '')
        if not plant_name:
            return jsonify({'error': 'Please provide a plant name to search for.'}), 400

        api_url = f"https://perenual.com/api/species-care-guide-list?key={api_key}&q={plant_name}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()  # Checks for HTTP request errors
            guides_data = response.json().get('data', [])

            # Prepare the guides data for response
            if guides_data:
                plants = []
                for guide in guides_data:
                    plant_info = {
                        'common_name': guide.get('common_name', 'Unknown'),
                        'scientific_name': guide.get('scientific_name', 'Unknown'),
                        'care_guides': []
                    }
                    for section in guide.get('section', [])[:3]:  # Limit to first 3 care guides
                        care_guide = {
                            'type': section.get('type', 'No type available'),
                            'description': section.get('description', 'No description available')
                        }
                        plant_info['care_guides'].append(care_guide)
                    plants.append(plant_info)
                return jsonify(plants)
            else:
                return jsonify({'message': 'No care guides found for the specified plant.'})
        except requests.RequestException as e:
            # Log the error and return a message
            print(f"Error fetching data: {str(e)}")
            return jsonify({'error': 'Failed to fetch data from Perennial API'}), 500



    @app.route('/api/bookmark', methods=['GET', 'POST'])
    @login_required
    def api_bookmark():
        data = request.json  # Parse JSON data from the request
        plant_name = data.get('plant_name')
        scientific_name = data.get('scientific_name')
        guide_type = data.get('guide_type')
        guide_description = data.get('guide_description')

        # Create a new bookmark object and add it to the database
        bookmark = Bookmark(
            plant_name=plant_name,
            scientific_name=scientific_name,
            guide_type=guide_type,
            guide_description=guide_description,
            user_id=current_user.id  # Assuming you have a user_id associated with the bookmarks
        )
        db.session.add(bookmark)
        db.session.commit()

        # Optionally, you can return a response to the client
        return jsonify({'message': 'Plant bookmarked successfully'})
        

    @app.route('/api/remove_bookmark', methods=['POST'])
    @login_required
    def api_remove_bookmark():
        bookmark_id = request.form.get('bookmark_id')
        bookmark = Bookmark.query.filter_by(id=bookmark_id, user_id=current_user.id).first()
        if bookmark:
            db.session.delete(bookmark)
            db.session.commit()
            flash('Bookmark removed successfully', 'success')
        else:
            flash('Bookmark not found or does not belong to the current user', 'error')
        return redirect(url_for('favorites'))


    return app

# Outside the create_app function to ensure the app is created at import time
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)