#Author Prasanna Hegde.
#from webdriver_manager.chrome import ChromeDriverManager
#import time
from bs4 import BeautifulSoup as bs

from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service

chrome_options=webdriver.ChromeOptions()
chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

def fetch_drug_image(drug_info:str,drug_dict):
    print("URl",drug_info)
    if drug_info != "None":
        try:
            # driver = webdriver.Chrome(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=Service(executable_path=os.environ.get("CHROMEDRIVER_PATH")), options=chrome_options)
            driver.get(drug_info)
            #stabalise
            #time.sleep(3)
            print(driver.title)
            driver.execute_script("window.scrollTo(0, 1000);")
            html = driver.page_source
            soup = bs(html, "html.parser")
            driver.close()
            driver.quit()
            if (soup.find("div", {"class": "imprint-image"})):
                image_url = soup.find_all("div", {"class": "imprint-image"})[0].img['src']
                image_alt = soup.find_all("div", {"class": "imprint-image"})[0].img['alt']
                drug_dict['image_url'] = image_url
                drug_dict['image_alt'] = image_alt
            else:
                drug_dict['image_url'] = None
                drug_dict['image_alt'] = "No Image Found"
            return drug_dict
        except:
            drug_dict['image_url'] = None
            drug_dict['image_alt'] = "No Image Found"
            return drug_dict


    else:
        drug_dict['image_url'] = None
        drug_dict['image_alt'] = "No Image Found"
        return drug_dict