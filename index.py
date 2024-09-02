from flask import Flask, request, jsonify
import requests
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    query = req.get('queryResult', {}).get('queryText', '')

    if "define" in query.lower() or len(query.split()) < 5:
        result = google_search(query)
    else:
        result = chatgpt_response(query)

    response = {
        "fulfillmentText": result
    }

    return jsonify(response)

def google_search(query):
    api_key = os.getenv('GOOGLE_API_KEY')
    search_engine_id = os.getenv('SEARCH_ENGINE_ID')
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={search_engine_id}&q={query}"
    response = requests.get(url)
    items = response.json().get('items', [])
    if items:
        return items[0]['snippet']
    return "No results found."

def chatgpt_response(query):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=query,
        max_tokens=100
    )
    return response.choices[0].text.strip()

@app.route('/', methods=['GET'])
def index():
    return "Flask app is running!"


if __name__ == '__main__':
    app.run(debug=True)
