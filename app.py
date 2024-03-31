# Make sure to import the necessary modules at the beginning of your app.py
from flask import Flask, render_template, request, jsonify
import os
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')  # Get the search query from the URL parameter
    if query:
        api_key = 'sk-uWoc66099b922db0a4934'  # Directly using the API key for demonstration; consider securing it for production
        results = fetch_plant_data(query, api_key)
        return render_template('search_results.html', query=query, results=results)
    return render_template('search.html')

def fetch_plant_data(query, api_key):
    headers = {'Authorization': f'Bearer {api_key}'}
    api_url = f'https://api.perenual.com/search?query={query}'  # Placeholder URL
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return []

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True)


