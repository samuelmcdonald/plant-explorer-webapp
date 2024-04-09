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
        return render_template('favorites.html')
            
    @app.route('/search')
    def search():
        return render_template('search.html')


    def fetch_species_id(api_key, plant_name):
        search_url = f"https://perenual.com/api/species-list?key={api_key}&q={plant_name}"
        response = requests.get(search_url)
        print("API Response:", response.text)  # Print API response
        if response.status_code == 200:
            species_data = response.json().get('data', [])
            if species_data:
                # Assuming the API returns the first species found
                return species_data[0].get('species_id')
        return None



    def fetch_care_guide(api_key, plant_id):
        guide_types = ['watering', 'sunlight', 'pruning']
        guide_details = {}

        for guide_type in guide_types:
            guide_url = f"https://perenual.com/api/species-care-guide-list?key={api_key}&type={guide_type}&species_id={plant_id}"
            try:
                response = requests.get(guide_url)
                response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
                
                print(f"{guide_type.capitalize()} Guide Response:", response.text)  # Print API response
                
                if response.status_code == 200:
                    guide_data = response.json().get('data', [])
                    if guide_data:
                        guide_details[guide_type] = guide_data[0].get('description')
                    else:
                        guide_details[guide_type] = 'No guide available.'
                else:
                    guide_details[guide_type] = 'Failed to fetch guide.'
                    
                print(f"{guide_type.capitalize()} Guide Details:", guide_details[guide_type])  # Print guide details
            except requests.RequestException as e:
                print(f"Error fetching {guide_type} guide:", e)
                guide_details[guide_type] = f"Error fetching {guide_type} guide: {str(e)}"
                
        return guide_details



    @app.route('/api/search', methods=['GET'])
    def api_search():
        query_params = {
            'q': request.args.get('q', ''),
            'page': request.args.get('page', 1),
            'order': request.args.get('order', 'asc'),
        }

        api_url = f"https://perenual.com/api/species-list?key={api_key}"
        for param, value in query_params.items():
            if value is not None:
                api_url += f"&{param}={value}"

        try:
            response = requests.get(api_url)
            response.raise_for_status()
            plants_data = response.json().get('data', [])

            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(fetch_care_guide, api_key, plant.get('species_id', '')): plant for plant in plants_data}
                for future in futures:
                    plant = futures[future]
                    guide_details = future.result()  # Fetch all guides
                    
                    # Update plant dictionary with fetched guides
                    plant.update(guide_details)

            # Construct the final plants list with required information
            plants = [{
                'common_name': plant['common_name'], 
                'scientific_name': plant['scientific_name'][0],
                'cycle': plant.get('cycle', 'Unknown'),  # Assuming you still want to include the cycle
                'watering_guide': plant.get('watering', 'No guide available.'),
                'sunlight_guide': plant.get('sunlight', 'No guide available.'),
                'pruning_guide': plant.get('pruning', 'No guide available.')  # Include pruning guide details
            } for plant in plants_data]

            return jsonify(plants)
        except requests.RequestException as e:
            print(e)
            return jsonify({'error': 'Failed to fetch data from Perennial API'}), 500



    return app

# Outside the create_app function to ensure the app is created at import time
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)