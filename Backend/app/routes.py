from flask import Blueprint, request, jsonify
from .scraper import scrape_data
from .chatgpt import run_single_call
import json
main = Blueprint('main', __name__)

@main.route('/search', methods=['POST'])
def search():
    try:
        data = request.json
        company = data.get("company")
        if not company:
            return jsonify({"error": "Company is required"}), 400

        # Scraper logic
        names, records = scrape_data(company)

        # ChatGPT API call
        chatgpt_response = run_single_call(names, company)


        result = [
            {'name': name,
             'email': chatgpt_response.get(name, 'Email not found'),
             'title': records.get(name, 'Title not found')
             }
            for name in names
        ]

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
