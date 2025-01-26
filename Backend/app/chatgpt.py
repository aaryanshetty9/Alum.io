from openai import OpenAI
import json
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found. Please set it in your .env file.")


OPENclient = OpenAI(api_key=OPENAI_API_KEY)

def run_single_call(names, company):
    prompt = f"""
    Given the names and company, generate a JSON object with the name of the person and their email address.
    Input:
    Names: {names}
    Company: {company}

    MAKE SURE THAT THE EMAIL FORMAT IS SPECIFIC TO THIS COMPANY. BE SURE TO CHECK THAT THE EMAIL IS VALID.

    Output format:
    {
        "name": "<email>",
        "name": "<email>",
        "name": "<email>"
    }
    """
    completion = OPENclient.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": prompt}]
    )

    response = completion.choices[0].message.content
    cleaned_response = response.replace("```json", "").replace("```", "")
    final_response = eval(cleaned_response)


    return final_response