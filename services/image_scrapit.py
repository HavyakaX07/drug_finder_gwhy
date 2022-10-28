#Author Prasanna Hegde.
from webdriver_manager.chrome import ChromeDriverManager
#import time
from bs4 import BeautifulSoup as bs

from selenium import webdriver
import os
from selenium.webdriver.chrome.service import Service
#
chrome_options=webdriver.ChromeOptions()
chrome_options.binary_location=os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(service=Service(executable_path=os.environ.get("CHROMEDRIVER_PATH")),
                                      options=chrome_options)

def fetch_drug_image(drug_info:str):
    drug_dict={}
    print("URl",drug_info)
    if drug_info != "None":
        try:
            # driver = webdriver.Chrome(ChromeDriverManager().install())
            driver.get(drug_info)
            #stabalise
            #time.sleep(3)
            # if driver.title == "WebMD Drugs & Medications - Medical information on prescription drugs, vitamins and over-the-counter medicines":
            #     drug_dict['image_url'] = None
            #     drug_dict['image_alt'] = "No Image Found"
            #     driver.close()
            #     driver.quite()
            #     return drug_dict
            driver.execute_script("window.scrollTo(0, 1000);")
            html = driver.page_source
            # driver.close()
            # driver.quit()
            soup = bs(html, "html.parser")
            if (soup.find("div", {"class": "imprint-image"})):
                image_urls=[]
                image_alts=[]
                image_url = soup.find_all("div", {"class": "imprint-image"})[0].img['src']
                image_alt = soup.find_all("div", {"class": "imprint-image"})[0].img['alt']
                image_urls.append(image_url)
                image_alts.append(image_alt)
                if(soup.find("div",{'class':"image-list"})):
                    all_images=soup.find_all("div",{"class":"image-list"})
                    for image in all_images:
                        image_url=image.img['src']
                        image_alt=image.img['alt']
                        image_urls.append(image_url)
                        image_alts.append(image_alt)
                    image_urls="<!sep!hegde!>".join(image_urls)
                    image_alts="<!sep!hegde!>".join(image_alts)
                    drug_dict['image_url']=image_urls
                    drug_dict['image_alt']=image_alts
                else:
                    image_urls.append("None")
                    image_alts.append("No Image Found")
                    drug_dict['image_url'] = image_urls
                    drug_dict['image_alt'] = image_alts

            else:
                drug_dict['image_url'] = "None"
                drug_dict['image_alt'] = "No Image Found"
            return drug_dict
        except Exception as e:
            print("Image fetching exception happend {}".format(e))
            drug_dict['image_url'] = "None"
            drug_dict['image_alt'] = "No Image Found"
            return drug_dict


    else:
        drug_dict['image_url'] = None
        drug_dict['image_alt'] = "No Image Found"
        return drug_dict

def create_driver():
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        return driver
    except Exception as e:
        print("Exception occured while creating the driver {}".format(e))
        return None
