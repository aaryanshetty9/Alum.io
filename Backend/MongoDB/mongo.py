from dotenv import load_dotenv
import os
from pymongo import MongoClient
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
from openai import OpenAI

load_dotenv(override=True)
Username = os.getenv('Username')
Password = os.getenv('Password')


def scrape_data(companies_links):
    temp_dir = tempfile.mkdtemp()
    options = Options()
    options.add_argument(f"--user-data-dir={temp_dir}")

    driver = webdriver.Chrome(options=options)

    driver.get(f"{companies_links[0]}/people/?facetSchool=5274&keywords=northeastern&viewAsMember=true")

    # Login handling
    driver.find_element(By.ID, "username").send_keys(Username)
    driver.find_element(By.ID, "password").send_keys(Password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    records = {}
    # names_list = []
    for link in companies_links:
        company_name = link.split('/')[-1] 
        records[company_name] = {}

        driver.get(f"{link}/people/?facetSchool=5274&keywords=northeastern&viewAsMember=true")

        try:
            container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "display-flex.list-style-none.flex-wrap"))
            )

            people_elements = container.find_elements(By.CLASS_NAME, "artdeco-entity-lockup__content.ember-view")
            for person in people_elements:
                name = person.find_element(By.CLASS_NAME, "artdeco-entity-lockup__title.ember-view").text or "Name not found"
                title = person.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle.ember-view").text or "Title not found"
                records[company_name][name] = title
                # names_list.append(name)
            sleep(2)
        except Exception as e:
            print(f"Error during scraping for {company_name}: {e}")
    driver.quit()
    # return names_list, records
    return records



def run_single_call_perp(Records,email_formats):
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    # url = "https://api.perplexity.ai/chat/completions"
    # headers = {"Authorization": f"Bearer {perp_api_key}"}
    messages = [
        {
            "role": "system",
            "content": "You are an artificial intelligence assistant tasked with processing JSON data."
        },
        {
            "role": "user",
            "content": (
                "Given a JSON object with companies, employees, and their titles, generate an identical JSON object "
                "but add an email field for each employee. Use the provided email formats to determine the correct email format for each company.\n\n"
                
                "These are the email formats:\n"
                f"{json.dumps(email_formats, indent=2)}\n\n"

                "This is the raw JSON file of companies and employees:\n"
                f"{json.dumps(Records, indent=2)}\n\n"

                "### Expected JSON Output Format\n"
                "The output should be a **valid JSON object** structured as follows:\n"
                "{\n"
                '      "Company": '
                    '        [\n'
                    '        {\n'
                    '          "name": "placeholder",\n'
                    '          "title": "placeholder",\n'
                    '          "email": "placeholder"\n'
                    '        },\n'
                    '        {\n'
                    '          "name": "placeholder",\n'
                    '          "title": "placeholder",\n'
                    '          "email": "placeholder"\n'
                '        }\n'
                '      ],\n'
                '      "Company": '
                    '        [\n'
                    '        {\n'
                    '          "name": "placeholder",\n'
                    '          "title": "placeholder",\n'
                    '          "email": "placeholder"\n'
                    '        },\n'
                    '        {\n'
                    '          "name": "placeholder",\n'
                    '          "title": "placeholder",\n'
                    '          "email": "placeholder"\n'
                '        }\n'
                '      ],\n'
                "}\n\n"

                "ONLY RETURN THE JSON, NO OTHER TEXT"
            )
        }
    ]
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model = 'gpt-4o',
        messages = messages,
        temperature=0.0
    )

    print(response)
    print(response.choices[0].message.content)
    message_response = response.choices[0].message.content
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
    # final_response = json.loads(message_response)
    # return final_response


    
    # print('test1')
    # response = requests.post(url, headers=headers, json=payload)
    # print('test2')
    # if response.status_code != 200:
    #     print(f"Error: API request failed with status code {response.status_code}")
    #     print(f"Response content: {response.text}")
    #     return None

    # response_data = response.json()
    # print('test3')

    # message_response = response_data["choices"][0]["message"]["content"]

    # cleaned_response = message_response.strip("`").strip()

    # final_response = json.loads(cleaned_response)
    # return final_response



linkedin_urls = [
    "https://www.linkedin.com/company/apple",
    "https://www.linkedin.com/company/microsoft",
    "https://www.linkedin.com/company/google",
    "https://www.linkedin.com/company/amazon",
    "https://www.linkedin.com/company/meta",
    "https://www.linkedin.com/company/nvidia",
    "https://www.linkedin.com/company/tesla-motors",
    "https://www.linkedin.com/company/ibm",
]


email_formats = {
    "Tesla": "[first_initial][last_name]@tesla.com",
    "SpaceX": "[first_name].[last_name]@spacex.com",
    "Apple": "[first_initial][last_name]@apple.com",
    "Google (Alphabet)": "[first_initial][last_name]@google.com",
    "Microsoft": "[first_name].[last_name]@microsoft.com",
    "Meta (Facebook)": "[first_name]@fb.com",
    "Amazon": "[last_name][first_initial]@amazon.com",
    "NVIDIA": "[first_initial][last_name]@nvidia.com",
    "OpenAI": "[first_name]@openai.com",
    "Palantir": "[first_initial][last_name]@palantir.com",
    "Square (Block)": "[first_initial][last_name]@block.xyz",
    "Discord": "[first_name].[last_name]@discord.com",
    "Airbnb": "[first_name].[last_name]@airbnb.com",
    "Uber": "[first_name]@uber.com",
    "Lyft": "[first_initial][last_name]@lyft.com",
    "Reddit": "[first_name].[last_name]@reddit.com",
    "Spotify": "[first_name][last_initial]@spotify.com",
    "Oracle": "[first_name].[last]@oracle.com",
    "Adobe": "[first_initial][last]@adobe.com",
    "Salesforce": "[first_initial][last]@salesforce.com",
    "Intel": "[first_name].[last]@intel.com",
    "Cisco Systems": "[first_initial][last]@cisco.com",
    "Stripe": "[first_name]@stripe.com",
    "Shopify": "[first_name].[last]@shopify.com",
    "Goldman Sachs": "[first_name].[last]@gs.com",
    "JPMorgan Chase": "[first_name].[last]@jpmchase.com",
    "Morgan Stanley": "[first_name].[last]@morganstanley.com",
    "Citadel": "[first_name].[last]@citadel.com",
    "BlackRock": "[first_name].[last]@blackrock.com",
    "Bridgewater Associates": "[first_name].[last]@bwater.com",
    "Vanguard": "[first_name]_[last]@vanguard.com",
    "Fidelity Investments": "[first_name].[last]@fmr.com",
    "Bank of America": "[first_name].[last]@bofa.com",
    "Wells Fargo": "[first_name].[last]@wellsfargo.com",
    "Barclays": "[first_name].[last]@barclays.com",
    "Credit Suisse": "[first_name].[last]@credit-suisse.com",
    "UBS": "[first_name].[last]@ubs.com",
    "Deutsche Bank": "[first_name].[last]@db.com",
    "HSBC": "[first_name].[last]@hsbcib.com",
    "Société Générale": "[first_name].[last]@socgen.com",
    "Charles Schwab": "[first_name].[last]@schwab.com",
    "TD Ameritrade": "[first_name].[last]@tdameritrade.com",
    "Nomura": "[first_name].[last]@nomura.com",
    "PIMCO": "[first_name].[last]@pimco.com",
    "Jane Street": "[first_initial][last]@janestreet.com",
    "Two Sigma": "[first_name].[last]@twosigma.com",
    "Renaissance Technologies": "[first_initial][last]@rentec.com",
    "DRW": "[first_initial][last]@drw.com",
    "Jump Trading": "[first_initial][last]@jumptrading.com",
    "Optiver": "[first_name].[last]@optiver.com",
    "Susquehanna International Group": "[first_name].[last]@sig.com",
    "IMC Trading": "[first_initial][last]@imc.com",
    "Hudson River Trading": "[first_name]@hudson-trading.com",
    "Akuna Capital": "[first_name].[last]@akunacapital.com",
    "IBM": "[first_initial].[last_name]@ibm.com"
}


    # "https://www.linkedin.com/company/oracle",
    # "https://www.linkedin.com/company/adobe",
    # "https://www.linkedin.com/company/salesforce",
    # "https://www.linkedin.com/company/intel-corporation",
    # "https://www.linkedin.com/company/cisco",
    # "https://www.linkedin.com/company/palantir-technologies",
    # "https://www.linkedin.com/company/spacex",
    # "https://www.linkedin.com/company/uber-com",
    # "https://www.linkedin.com/company/airbnb",
    # "https://www.linkedin.com/company/stripe",
    # "https://www.linkedin.com/company/shopify",
    # "https://www.linkedin.com/company/spotify",
    # "https://www.linkedin.com/company/goldman-sachs",
    # "https://www.linkedin.com/company/jpmorgan-chase",
    # "https://www.linkedin.com/company/morgan-stanley",
    # "https://www.linkedin.com/company/citadel-llc",
    # "https://www.linkedin.com/company/blackrock",
    # "https://www.linkedin.com/company/bridgewater-associates",
    # "https://www.linkedin.com/company/vanguard",
    # "https://www.linkedin.com/company/fidelity-investments",
    # "https://www.linkedin.com/company/bank-of-america",
    # "https://www.linkedin.com/company/wells-fargo",
    # "https://www.linkedin.com/company/barclays",
    # "https://www.linkedin.com/company/credit-suisse",
    # "https://www.linkedin.com/company/ubs",
    # "https://www.linkedin.com/company/deutsche-bank",
    # "https://www.linkedin.com/company/hsbc",
    # "https://www.linkedin.com/company/societe-generale",
    # "https://www.linkedin.com/company/charles-schwab",
    # "https://www.linkedin.com/company/td-ameritrade",
    # "https://www.linkedin.com/company/nomura",
    # "https://www.linkedin.com/company/pimco",
    # "https://www.linkedin.com/company/jane-street",
    # "https://www.linkedin.com/company/two-sigma-investments",
    # "https://www.linkedin.com/company/renaissance-technologies",
    # "https://www.linkedin.com/company/drw",
    # "https://www.linkedin.com/company/jump-trading",
    # "https://www.linkedin.com/company/optiver",
    # "https://www.linkedin.com/company/susquehanna-international-group",
    # "https://www.linkedin.com/company/imc",
    # "https://www.linkedin.com/company/hudson-river-trading",
    # "https://www.linkedin.com/company/akuna-capital"








# Records=scrape_data(linkedin_urls)
# print(Records)

# with open('MongoDB.json', 'w') as f:
#     Records = json.load(f)

Records = {'apple': {'Livia Sanjeev Gonsalves': 'Site Reliability Engineer at Apple', 'Kanachi W.': 'Software Engineer @Apple | Computer Engineering, Data Science @ Northeastern University', 'Pranjal Rane': 'Software Engineer @ Apple | MS CS @ Northeastern University', 'Priyank Sanjay': 'Staff Software Engineer at Apple', 'Pulkit J.': 'Software Engineer at Apple', 'Saad Mobarak': 'MechE @ Northeastern | prev @ Apple & Tesla', 'Xikai Liu': 'Software Engineer @ Apple', 'Reza Asadi': 'Staff Software Engineer at Apple', 'Dhanisha Phadate': 'SRE @ Apple \uf8ff', 'Juan Garibay Atef': 'Finance Student at Northeastern University', 'Ryan Tsai': 'SWE Intern @ Apple | CS @ Northeastern University', 'Sam Scroggie': 'Camera Process Engineer @ Apple | Stamps Scholar @ Northeastern University'}, 'microsoft': {'Sydney Nguyen': 'CS + Cognitive Science @ Northeastern', 'Varsha Jain': 'Software Engineer II at Microsoft', 'Ankit Masrani': 'Principal Engineer at Microsoft', 'Wendi O.': 'SWE @ Microsoft', 'Sekou Samassi': 'Incoming Explore Intern @ Microsoft | CS + Design @ Northeastern University | Rales Scholar', 'Akshay Relekar': 'Software Engineer 2 at Microsoft', 'Cindy Chen': 'CS @ NEU | Incoming SWE Co-op @ UEI | Incoming SWE Intern @ Microsoft', 'Isabel B.': 'Product at Microsoft', 'Shakti Chetan Rao': 'Software Engineer @ Microsoft | Ex-Amazon | Kubernetes |', 'Deepak Sharma': 'Software Developer II at Microsoft', 'Gaurav A.': 'Principal Software Engineer at Microsoft Teams, Ex-Salesforce, Ex-Amazon', 'Yishu Xu': 'Senior SDE at Azure SQL; actively looking for new opportunities'}, 'google': {'Sunjit Dhillon': 'Software Engineer @Google', 'Emiliano (Zhenfang) Zhu': 'Software Engineer at Google | Cloud Billing', 'Abdoul-hanane Gbadamassi': 'SWE,ML @Google | Master in CS at Northeastern University | x-Bloomberg SWE | x-Google TnS YouTube Monetization Data & Insight Intern | x-Data Science + CS at Claremont McKenna College', 'Palak Mundra': '🚀 Cloud Solutions Architect | Software Engineer | Multi-Cloud Expert | Driving Innovation and Automation', 'Shivam Thakur': 'Software and ML at Google Cloud', 'Parshva Timbadia': 'Software Engineer @Google | Ex-SWE @Meta,CarGurus', 'Neha Shewani': 'Software Engineer at Google', 'Diego Rivas': 'Senior Product Manager at Google', 'Xiaomai C.': 'User Experience Researcher, Gemini @Vertex AI', 'Sydney Bao': 'Incoming SWE Intern at Google | Computer Science and Design @ Northeastern University', 'Aishwarya Murali': 'Software Engineer | Android', 'Shubham Bhagwat': 'Cloud @ Google | Ex-BMW Group | MS Data Science @Northeastern University'}, 'amazon': {'Varun Morishetty': 'SDE @ Amazon | CS @ Northeastern University', 'Kanika Makhija': 'Software Development Engineer at Amazon Web Services (AWS)', 'Shravya Cherukuri': 'Frontend Engineer @ AWS | UX Designer | Salesforce Certified', 'Akarsh C.': 'SDE @ Amazon Prime Video | CS @ Northeastern University | Android | Cloud | AI', 'Chetan Nigudgi': 'Software Dev Engineer | AWS | Northeastern University Alumni', 'Simran Goindani': "Data Scientist at AWS | Amazon | MFS Investment Management | Master's Graduate in Data Science from Northeastern University | Data Science | Machine Learning | Artificial Intelligence", 'Swati Bhojwani': 'Software Development Engineer || , AWS | Graduate Teaching Assistant | #GHC20 | Northeastern University 2021 | Ex-Lead Software Developer | JAVA,J2EE | SPRING | HIBERNATE | NODEJS | RUST', 'Sarthak Grover': 'Software Development Engineer II at Amazon', 'Sameer Singh': 'Software at AWS | Northeastern', 'Arvind Sudheer': 'SDE @ Amazon | Northeastern University', 'Siddhanth Jayaraj Ajri': 'SDE @ Amazon | Prev: @Oracle, @Unqork | Northeastern Alum', 'Prabhpreet Singh Dhillon': 'Amazon | SDE | Northeastern University | MS Computer Science | Class of 2020'}, 'meta': {'Manan Patel': 'Senior Software Engineer at Meta | Ex Google & AWS', 'Jing Fu': 'Software engineer at Meta', 'Shitan(Stan) Yang': 'Software Engineer at Meta', 'Shubham Muttepawar': 'Senior Software Engineer at Meta | Distributed Systems', 'Walker S.': 'Software Engineer @ Meta', 'Lingmiao Emma Q.': 'Engineering @ Meta', 'Yue Liu': 'Manager, AR AI at Meta', 'Abhilash Mysore Somashekar': 'Engineering @ Meta', 'Hari Panjwani': 'Facebook | AWS | Ads Infra | Java & Spark | NLP | Distributed Systems', 'Praveen Kumar Sridhar': 'Machine Learning @ Meta | Ex-[Nextdoor, Citizen] | NLP Research @ NEU', 'Nimesh Rajal': 'Data Engineer @ Meta | Data Engineer', 'Sally Wang': 'Web Developer | Full-stack | Alumni at Northeastern University'}, 'nvidia': {'Myrna V.': 'Data Scientist at NVIDIA', 'Kenneth Le': 'SOX Compliance Analyst at NVIDIA', 'Anubhuti V.': 'Software Engineer | Nvidia', 'Ajay Sureka': 'Senior Software Engineer @ NVIDIA || Full Stack Developer || Embedded Software Engineer || JAVA || SpringBoot || React || JavaScript || AWS || Distributed Systems', 'Mert Bozbeyoglu': 'Firmware Engineer @ NVIDIA', 'Andrew Tu': 'Senior Software Engineer, 3D Mapping | NVIDIA', 'Blake McHale': 'Robotics Systems Software Engineer at NVIDIA', 'Fengqi Qiao': 'SWE @ Nvidia', 'Suhas Maddali': 'Data Scientist @ NVIDIA | Large Language Models (LLMs) | Generative AI | MS in Data Science', 'Sanjana K.': 'Software Engineer', 'Xuangui Huang': 'AI DevTech Engineer @NVIDIA | CS Theory PhD @Northeastern | CS MS, BS @SJTU', 'Curt Lockhart': 'Senior AI Solutions Architect at NVIDIA'}, 'tesla-motors': {'Siddhartha Bariker': 'Engineer @ Tesla', 'Divya Bhupinder Suri': "SDE II @ Tesla | Former Software Engineer at Rockmetric | Graduate Student at Northeastern University '24 | AWS Certified Cloud Practitioner", 'Sindhya Balasubramanian': 'Data Scientist | Expertise in Machine Learning, Time Series Analysis, and NLP | MS in Data Science', 'Samarth Gowdra Shashi Kiran': 'Software Product Manager Intern @ Tesla | Driving User-Centric Innovation from Concept to Launch | MS Engineering Management student @ Northeastern University', 'Pranamya .': 'Tesla | Northeastern University', 'Grant Ritter': 'Senior Mechanical Design Engineer at Tesla Design Studio', 'Niyati Khandelwal': 'Software Engineer @ Tesla | Prev @ Lumen, IBM | Full Stack Developer | MSCS @ Northeastern University, Khoury College of Computer Sciences', 'Aditya A.': "Sr. Logistics Data Analyst at Tesla | Master's Degree at Northeastern University", 'Mark Wang': 'Sr Data Scientist at Tesla', 'Jamie P.': 'Product Intern @ Tesla | Prev. Microsoft', 'Lillian Lema': 'Material Planning Intern @ Tesla | MPS Graduate Student at Northeastern University', 'Joshua Joseph': 'Manufacturing Process @ Tesla'}, 'ibm': {'Thierno Ahamadou Bah': 'IBM Software Developer | Computer Science Alumni at Northeastern University', 'Aly Badary': 'DevOps Developer @ IBM', 'Maddison Niebling': 'Consultant @ IBM | 4x Salesforce Certified', 'Ben Wolpert': 'Consultant at IBM', 'Sriram Voruganti': 'Software Developer at IBM || Graduate @ Northeastern || BITS Pilani', 'Aiyan Jiang': 'SWE @ IBM | CS @ Northeastern', 'Akshay Dangare': 'Staff Software Engineer @ IBM | Cloud Infrastructure', 'Habeebuddin Mir': 'Software Developer at IBM', 'Asha Padmashetti': 'Staff Software Developer @IBM', 'Ankur Verma': 'Staff Software Engineer at IBM', 'Tobias Barker': 'Associate Consultant at IBM', 'Alexander Wu': 'Consultant @ IBM | 8x Salesforce Certified'}}


perp_call = run_single_call_perp(Records,email_formats)
print(perp_call)

try:
    with open('MongoDB.json', 'w') as f:
        json.dump(perp_call, f)
except TypeError as e:
    # Handle the case where `perp_call` is not serializable
    print(f"JSON serialization failed: {e}. Saving raw string instead.")
    with open('MongoDB.json', 'w') as f:
        f.write(str(perp_call))
except Exception as e:
    # Handle unexpected errors
    print(f"Unexpected error while saving to file: {e}")
