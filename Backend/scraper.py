from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tempfile
from dotenv import load_dotenv
from MongoDB.client import get_linkedin_link


import os

load_dotenv(override=True)
Username = os.getenv('Username')
Password = os.getenv('Password')


def scrape_data(company):
    temp_dir = tempfile.mkdtemp()
    options = Options()
    options.add_argument(f"--user-data-dir={temp_dir}")

    driver = webdriver.Chrome(options=options)
    linkedin_link = get_linkedin_link(company)
    driver.get(f"{linkedin_link}people/?facetSchool=5274&keywords=northeastern&viewAsMember=true")

    # Login handling
    driver.find_element(By.ID, "username").send_keys(Username)
    driver.find_element(By.ID, "password").send_keys(Password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    records = {}
    names_list = []

    try:
        container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "display-flex.list-style-none.flex-wrap"))
        )

        people_elements = container.find_elements(By.CLASS_NAME, "artdeco-entity-lockup__content.ember-view")
        for person in people_elements:
            name = person.find_element(By.CLASS_NAME, "artdeco-entity-lockup__title.ember-view").text or "Name not found"
            title = person.find_element(By.CLASS_NAME, "artdeco-entity-lockup__subtitle.ember-view").text or "Title not found"
            records[name] = title
            names_list.append(name)
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        driver.quit()

    return names_list, records