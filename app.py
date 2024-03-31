from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Existing route for rendering index.html
@app.route('/')
def index():
    return render_template('index.html')

# New route for handling recipe search request
@app.route('/get_recipe', methods=['POST'])
def get_recipe():
    dish = request.form['dish']
    recipe_data = fetch_recipe(dish)
    return jsonify(recipe_data)

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
            ingredients = [meal[f'strIngredient{i}'] for i in range(1, 21) if meal[f'strIngredient{i}']]
            return {'title': title, 'instructions': instructions, 'ingredients': ingredients}
        else:
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
