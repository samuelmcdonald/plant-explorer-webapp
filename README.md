# Plant Explorer Webapp

Welcome to the Plant Explorer Webapp project! This application is designed to help users explore various plants, manage their favorites, and learn more about plant care.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- pip (Python package installer)
- Virtualenv (optional but recommended for managing project dependencies)

### Installing

Follow these steps to get your development environment set up:

1. **Clone the repository**
```
git clone https://github.com/<your-username>/plant-explorer-webapp.git
```
2. **Navigate to the project directory**
```
cd plant-explorer-webapp
```
3. **Create a virtual environment (Optional)**

- For Windows:
  ```
  python -m venv venv
  ```
- For macOS and Linux:
  ```
  python3 -m venv venv
  ```

4. **Activate the virtual environment**

- On Windows:
  ```
  .\venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

5. **Install the required packages**
```
pip install -r requirements.txt
```
### Database Initialization
After installing the required packages, you'll need to set up the database before running the application. Follow these steps to initialize your database:

1. **Initialize the database migration environment**
```
flask db init
```
2. **Generate an initial database migration**
```
flask db migrate -m "Initial migration."
```
3. **Apply the migration to the database**
```
flask db upgrade
```
These commands prepare your database for use with the application by creating the necessary tables and schema.

# Viewing the database
To view a physical version of the database, download SQLite for your desktop, and click the "load database" button, then select the instance folder and 
upload the "plantexplorer.db" file. Now you can use SQL queries to view the contents of your database as well as its structure

### Running the Application

With your virtual environment activated and dependencies installed, you can run the Flask application using the following command:
```
flask run
```
Or you can use:
```
python -m flask run
```
This will start the Flask development server, and you should see output indicating it's running on `http://127.0.0.1:5000/`. Open this URL in your web browser to view the application.

## Authors

- **Samuel McDonald** - *Created application and leveraged API* - [samuelmcdonald](https://github.com/samuelmcdonald)
- **Ulysses Bueno** - [TeamMemberUsername](https://github.com/TeamMemberUsername)
- **Gurkeerat Bains** - [TeamMemberUsername](https://github.com/TeamMemberUsername)
