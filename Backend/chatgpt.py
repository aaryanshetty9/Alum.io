from openai import OpenAI
import json
from dotenv import load_dotenv
import os


def run_single_call(names, company):
    load_dotenv(override=True)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    print(OPENAI_API_KEY)


    OPENclient = OpenAI(api_key=OPENAI_API_KEY)

    prompt = f"""
    Given the names and company, generate a JSON object with the name of the person and their email address.
    Input:
    Names: {names}
    Company: {company}

    MAKE SURE THAT THE EMAIL FORMAT IS SPECIFIC TO THIS COMPANY. BE SURE TO CHECK THAT THE EMAIL IS VALID.

    Output format:
    {{
        "name": "<email>",
        "name": "<email>",
        "name": "<email>"
    }}

    DONT OUTPUT ANYTHING ELSE THAN THE JSON.
    """
    try:
        completion = OPENclient.chat.completions.create(
            model='gpt-4o',
            messages=[{"role": "user", "content": prompt}]
        )

        response = completion.choices[0].message.content
        cleaned_response = response.strip()
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response[7:]
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response[:-3]
        cleaned_response = cleaned_response.strip()
        
        # Parse JSON instead of using eval
        try:
            final_response = json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Response was: {cleaned_response}")
            return {}  # Return empty dict if parsing fails
        
        print(final_response)
            
        return final_response

    except Exception as e:
        print(f"Error in ChatGPT call: {e}")
        return {}  # Return empty dict if anything fails