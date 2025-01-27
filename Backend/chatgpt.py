from openai import OpenAI
import json
from dotenv import load_dotenv
import os
from pydantic import BaseModel
import requests

class AnswerFormat(BaseModel):
    name: str
    email: str
    url: str

def run_single_call_perp(names, company):
    load_dotenv(override=True)
    perp_api_key = os.getenv('Perp_API_KEY')
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {perp_api_key}"}
    payload = {
        "model": "sonar",
        "messages": [
            {"role": "system", "content": "Be precise and concise."},
            {"role": "user", "content": (
                f"Given the names and company, generate a JSON object with the name of the person and their email address. "
                "MAKE SURE THAT THE EMAIL FORMAT IS SPECIFIC TO THIS COMPANY. Use the most common email format for this company."
                "Input: "
                f"Names: {names}"
                f"Company: {company}"
                "Please output a JSON object containing the following fields: "
                "Name, email. "
                "DONT OUTPUT ANYTHING ELSE THAN THE JSON. Make sure the JSON is valid and not in a list."
                "This is how it should look like: {{'name': 'EMAIL', 'name': 'EMAIL', 'name': 'EMAIL'}}"
            )},
        ],
        "response_format": {
                "type": "json_schema",
            "json_schema": {"schema": AnswerFormat.model_json_schema()},
        },
    }
    response = requests.post(url, headers=headers, json=payload).json()
    print(response)
    message_response = response["choices"][0]["message"]["content"]

    cleaned_response = message_response.strip()
    if cleaned_response.startswith('```json'):
        cleaned_response = cleaned_response[7:]
    if cleaned_response.endswith('```'):
        cleaned_response = cleaned_response[:-3]
    cleaned_response = cleaned_response.strip()
    
    try:
        final_response = json.loads(cleaned_response)
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}")
        print(f"Response was: {cleaned_response}")
        return {}
    
        
    return final_response