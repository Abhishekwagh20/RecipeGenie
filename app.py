from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Function to store previous search recipes in a file
def store_previous_searches(previous_searches):
    with open('previous_searches.json', 'w') as file:
        json.dump(previous_searches, file)

# Function to load previous search recipes from file
def load_previous_searches():
    try:
        with open('previous_searches.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Existing route for rendering index.html
@app.route('/')
def index():
    # Load previous search recipes
    previous_searches = load_previous_searches()
    return render_template('index.html', previous_searches=previous_searches)

# New route for handling recipe search request
@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    dish = request.form['dish']
    recipe_data = fetch_recipe(dish)
    
    # Store the current search in previous searches
    previous_searches = load_previous_searches()
    previous_searches.append({'search_term': dish, 'recipe': recipe_data})
    store_previous_searches(previous_searches)

    return jsonify(recipe_data)

# New route to fetch previous search recipes
@app.route('/previous_searches')
def previous_searches():
    previous_searches = load_previous_searches()
    return jsonify(previous_searches)

# New route to delete previous search recipes
@app.route('/delete_previous_recipes', methods=['DELETE'])
def delete_previous_recipes():
    store_previous_searches([])
    return 'Previous recipes deleted successfully'

def fetch_recipe(dish):
    url = f'https://www.themealdb.com/api/json/v1/1/search.php?s={dish}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        if 'meals' in data and data['meals']:
            meal = data['meals'][0]  # Assuming you want the first result
            title = meal['strMeal']
            instructions = meal.get('strInstructions', 'Instructions not available')
            ingredients = [meal[f'strIngredient{i}'] for i in range(1, 21) if meal.get(f'strIngredient{i}', '')]
            return {'title': title, 'instructions': instructions, 'ingredients': ingredients}
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
