from pymongo import MongoClient
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tempfile
from dotenv import load_dotenv
import json
from pydantic import BaseModel
import requests
from time import sleep
from typing import Dict, List, Optional
from groq import Groq
import time
from openperplex import OpenperplexSync


load_dotenv()

# Add error handling for MongoDB connection
try:
    mongo_uri = os.getenv('MONGO_URI')
    if not mongo_uri:
        raise ValueError("MONGO_URI environment variable is not set")
    
    # Add connection options for better reliability
    print('trying to connect to mongo')
    client = MongoClient(mongo_uri, 
                        serverSelectionTimeoutMS=5000,  # 5 second timeout
                        connectTimeoutMS=5000)
    print('connected to mongo')
    # Test the connection
    client.server_info()  # This will raise an exception if connection fails
    print('server info')
    db = client['AlumIO']
    alumni_collection = db['alumni']
    
except Exception as e:
    print(f"Failed to connect to MongoDB: {str(e)}")
    raise


school_name = "Northeastern University"  # Change based on your need


def add_Companies_data_to_db(school_name, Raw):
    formatted_data = {
        "school": school_name,
        "companies": [{"name": company, "employees": employees} for company, employees in Raw.items()]
    }

    # alumni_collection.insert_one(formatted_data)


    alumni_collection.update_one(
        {"school": school_name},
        {"$push": {"companies": formatted_data}}
    )
    print('Data Saved into DB!')
    return

def add_data_to_db(school_name, Raw):
    new_company = {
        "name": Raw.keys()[0],
        "employees": Raw
    }

    alumni_collection.update_one(
        {"school": school_name},
        {"$push": {"companies": new_company}}
    )
    print('Data Saved into DB!')
    return

def get_data_from_db(company_name):
    result = alumni_collection.find_one(
        {"school": "Northeastern University", "companies.name": company_name},
        {"_id": 0, "companies.$": 1}  # Only return the matched company
    )

    print(result)
    if result:
        employees = result["companies"][0]["employees"]
        print(employees)
        return employees
    else:
        return []


def get_linkedin_link(company_name):
    client = Groq(api_key=os.getenv('GROQ_API_KEY'))
    start_time = time.time()
    chat_completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": f"give me the linkedin link of {company_name}. ONLY RETURN THAT LINK. MAKE SURE THE LINK IS CORRECT. If the company is mispelled, correct company name."}],
    )
    end_time = time.time()
    print(f"Time taken: {end_time - start_time} seconds")
    test = ""
    test += chat_completion.choices[0].message.content
    print(test)
    return test

# api_key = os.getenv('OPENPERPLEX_API_KEY')
# client_sync = OpenperplexSync(api_key=api_key)

# start_time = time.time()

# result = client_sync.search(
#     query="can you find me with the LinkedIn URL of the company C3AI? ONLY RETURN THE LINK",
#     date_context="2024-08-25",
#     location="us",
#     pro_mode=False,
#     response_language="en",
#     answer_type="text",
#     verbose_mode=False,
#     search_type="general",
#     return_citations=False,
#     return_sources=False,
#     return_images=False,
#     recency_filter="anytime"
# )

# print(result['llm_response'])
# end_time = time.time()
# print(f"Time taken: {end_time - start_time} seconds")
