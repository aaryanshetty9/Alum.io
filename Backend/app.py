from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_data
from chatgpt import run_single_call
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(override=True)
app = Flask(__name__)

# Simplest CORS configuration - allow all origins during development
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route('/api/search', methods=['POST'])
def search():
    print("Received search request")
    try:
        data = request.json
        print("Request data:", data)
        
        company = data.get("company")
        if not company:
            return jsonify({"error": "Company is required"}), 400

        print(f"Searching for company: {company}")
        
        # Scraper logic
        names, records = scrape_data(company)
        print(f"Found {len(names)} names")

        # ChatGPT API call
        chatgpt_response = run_single_call(names, company)
        print("ChatGPT response received")

        result = [
            {'name': name,
             'email': chatgpt_response.get(name, 'Email not found'),
             'title': records.get(name, 'Title not found')
             }
            for name in names
        ]

        return jsonify(result)

    except Exception as e:
        print(f"Error in search: {str(e)}")
        return jsonify({"error": str(e)}), 500
    

@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
