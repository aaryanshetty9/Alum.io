# import sys
# print(sys.executable)

from flask import Flask, request, jsonify
from flask_cors import CORS
from scraper import scrape_data
from chatgpt import run_single_call_perp
import os
from dotenv import load_dotenv
from MongoDB.client import get_data_from_db
from MongoDB.client import add_data_to_db
from autocorrect import Speller
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
        
        company = company.lower()

        # Uncomment and use if spelling correction is needed
        # spell = Speller()
        # if company != spell(company):
        #     company = spell(company)

        employees = get_data_from_db(company)
        print(f'employees: {employees}')
        if employees:
            print('employees found')
            return jsonify(employees)
        
        print(f"Searching for company: {company}")
        
        # Scraper logic
        names, records = scrape_data(company)
        print(f"Found {len(names)} names")
        if not names:
            return jsonify({"error": "No names found"}), 400
        
        # ChatGPT API call
        chatgpt_response = run_single_call_perp(names, company)

        result = [
            {'name': name,
             'email': chatgpt_response.get(name, 'Email not found'),
             'title': records.get(name, f'@ {company}')
            }
            for name in names
        ]
        MongoDict = {
            company: result
        }
        
        add_data_to_db(company, MongoDict)
        return jsonify(result)

    except Exception as e:
        print(f"Error in search: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({"message": "Hello, World!"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)