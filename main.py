import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

CAPACITIES_TOKEN = os.environ.get('CAPACITIES_TOKEN')
CAPACITIES_API = "https://api.capacities.io/v1"

def get_headers():
    return {
        "Authorization": f"Bearer {CAPACITIES_TOKEN}",
        "Content-Type": "application/json"
    }

@app.route('/')
def home():
    return {"status": "online", "endpoints": ["/test", "/search", "/create"]}

@app.route('/test')
def test():
    try:
        response = requests.get(f"{CAPACITIES_API}/objects", headers=get_headers(), params={"limit": 1}, timeout=30)
        response.raise_for_status()
        return {"success": True, "message": "Capacities API OK"}
    except Exception as e:
        return {"success": False, "error": str(e)}, 500

@app.route('/search', methods=['POST'])
def search():
    try:
        data = request.get_json()
        query = data.get('query', '')
        response = requests.get(f"{CAPACITIES_API}/search", headers=get_headers(), 
                              params={"q": query, "limit": 10}, timeout=30)
        response.raise_for_status()
        return {"success": True, "data": response.json(), "query": query}
    except Exception as e:
        return {"success": False, "error": str(e)}, 500

@app.route('/create', methods=['POST'])
def create():
    try:
        data = request.get_json()
        note_data = {
            "type": "note",
            "title": data.get('title', 'Nova Nota'),
            "content": data.get('content', ''),
            "tags": data.get('tags', [])
        }
        response = requests.post(f"{CAPACITIES_API}/objects", headers=get_headers(), 
                               json=note_data, timeout=30)
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except Exception as e:
        return {"success": False, "error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
