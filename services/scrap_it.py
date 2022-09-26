# Author Prasanna Hegde
# Actual scrapping of the web happens here.
import time

import requests as rq
from bs4 import BeautifulSoup as bs
# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager

from services import image_scrapit as img_scrap

siteurl = "https://www.webmd.com"
base_url = "https://www.webmd.com/drugs/2/search?type=conditions&query="
agent = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
all_drug_list = []


def initial_search(search_url: str):
    try:
        search_response1 = rq.get(search_url, headers=agent)
        beauty_search_res = bs(search_response1.text, "html.parser")
        search_response1.close()
        search_result_diseases = beauty_search_res.find_all("a", {"class": "common-drug-name"})
        disease_search = []
        for disease in range(len(search_result_diseases)//2):
            url = search_result_diseases[disease]
            dict_disease = {}
            dict_disease["name"] = url.text
            dict_disease["url"] = url['href']
            # print(url)
            # print(type(url))
            disease_search.append(dict_disease)
        return disease_search
    except:
        return []


# def fetch_drug_image(drug_info:str,drug_dict):
#     if drug_info != "None":
#         driver=None
#         try:
#             driver=webdriver.Chrome(ChromeDriverManager().install())
#         except Exception as exc:
#             print(exc)
#         driver.get(drug_info)
#         time.sleep(5)
#         driver.execute_script("window.scrollTo(0, 1000);")
#         html = driver.page_source
#         soup = bs(html, "html.parser")
#         if (soup.find("div", {"class": "imprint-image"})):
#             image_url = soup.find_all("div", {"class": "imprint-image"})[0].img['src']
#             image_alt = soup.find_all("div", {"class": "imprint-image"})[0].img['alt']
#             drug_dict['image_url'] = image_url
#             drug_dict['image_alt'] = image_alt
#         else:
#             drug_dict['image_url'] = None
#             drug_dict['image_alt'] = "No Image Found"
#         return drug_dict
#     else:
#         drug_dict['image_url'] = None
#         drug_dict['image_alt'] = "No Image Found"
#         return drug_dict


def find_drug_rating(rating_url, drug_info_url, drug_dict):
    if rating_url != "None" and drug_info_url != "None":
        drug_rating_res = rq.get(rating_url, headers=agent)
        # print(drug_rating_res)
        drug_rating_html = bs(drug_rating_res.text, "html.parser")
        # print(drug_rating_html)
        if (drug_rating_html.find("div", {"class": "review-page-content"})):
            rating = drug_rating_html.find("span", {"class": "rat-num"}).text
            # print("Overall Rating of the drug is ", rating)
            drug_dict['rating'] = str(rating)
        else:
            # print("No rating")
            drug_dict['rating'] = "No rating"
            #return drug_dict
        return img_scrap.fetch_drug_image(drug_info_url, drug_dict)
    else:
        drug_dict['rating'] = "No rating"
        #return drug_dict
        return img_scrap.fetch_drug_image("None",drug_dict)


def fetch_drug_detailed_info(drug_info_url, drug_dict):
    drug_info_res = rq.get(drug_info_url, headers=agent)
    drug_info_html = bs(drug_info_res.text, "html.parser")
    drug_info_res.close()
    if (drug_info_html.find("div", {"class": "uses-container"})):
        uses_model = drug_info_html.find_all("div", {"class": "uses-container"})
        uses_model = uses_model[0].find_all("div", {"class": "monograph-content"})
        uses_model = uses_model[0].find_all("p", {"class": ""})
        uses_string = ""
        if (uses_model[0].text == "See also Warning section."):
            for uses in range(1, len(uses_model)):
                uses_string += uses_model[uses].text
            # print("How to use-->", uses_string)
            drug_dict["how_to_use"] = uses_string
        else:
            for uses in range(0, len(uses_model)):
                uses_string += uses_model[uses].text
            # print("How to use-->", uses_string)
            drug_dict["how_to_use"] = uses_string
        side_effect_model = drug_info_html.find_all("div", {"class": "side-effects-container"})
        side_effect_model = side_effect_model[0].find_all("div", {"class": "monograph-content"})
        side_effect_model = side_effect_model[0].find_all("p", {"class": ""})
        side_effect_string = ""
        if (side_effect_model[0].text == "See also Warning section."):
            for side_effect in range(1, len(side_effect_model)):
                side_effect_string += side_effect_model[side_effect].text
            # print("Side effedt-->", side_effect_string)
            drug_dict['side_effect'] = side_effect_string
        else:
            for side_effect in range(0, len(side_effect_model)):
                side_effect_string += side_effect_model[side_effect].text
            # print("Side effect-->", side_effect_string)
            drug_dict['side_effect'] = side_effect_string
        rating_url = siteurl + \
                     drug_info_html.find_all("ul", {"class": "auto-tabs"})[0].find_all("li", {"class": ""})[0].a['href']
        return find_drug_rating(rating_url, drug_info_url, drug_dict)

    else:
        # print("No drug info")
        drug_dict['how_to_use'] = "No Description About How To Use This Drug"
        drug_dict['side_effect'] = "No Details About Side Effect Of This Drug"

        return find_drug_rating("None", "None", drug_dict)


def find_drug_basic_info(search_url):
    html_disease_response = rq.get(search_url, headers=agent)
    beauty_disease_response = bs(html_disease_response.text, "html.parser")
    html_disease_response.close()
    drug_list = beauty_disease_response.find_all("div", {"class": "table-content"})
    if(len(drug_list)!=0):
        # Only taking top 25 if more than 25 drugs because of some limitations
        if (len(drug_list) > 5):
            drug_list = drug_list[0:5]
        for drug in drug_list:
            drug_dict = {}
            drug_name = drug.span.text
            # fetch_drug_details
            drug_label = drug.find_all("span", {"class": "label-info"})[0].text
            drug_type = drug.find_all("span", {"class": "drug-type"})[0].text
            drug_dict['drug_name'] = drug_name
            drug_dict['drug_label'] = drug_label
            drug_dict['drug_type'] = drug_type
            drug_info = drug.span.a['href']
            drug_info = siteurl + drug_info
            tem_drug_dict = fetch_drug_detailed_info(drug_info, drug_dict)
            print(tem_drug_dict)
            all_drug_list.append(tem_drug_dict)
        return all_drug_list
    else:
        t_body = beauty_disease_response.find_all("tbody", {"class": ""})
        t_row = t_body[0].find_all("tr", {"class": ""})
        if(len(t_row)>5):
            t_row=t_row[0:5]
        for each_row in t_row:
            drug_dict = {}
            t_data = each_row.find_all("td", {"class": ""})
            drug_name = t_data[0].text
            drug_info = t_data[0].a['href']
            #print(drug_name)
            drug_dict['drug_name'] = drug_name
            #print(drug_info)
            drug_label = t_data[1].text
            #print(drug_label)
            drug_dict['drug_label'] = drug_label
            drug_type = t_data[2].text
            #print(drug_type)
            drug_dict['drug_type'] = drug_type
            drug_info = siteurl + drug_info
            tem_drug_dict = fetch_drug_detailed_info(drug_info, drug_dict)
            #print(tem_drug_dict)
            all_drug_list.append(tem_drug_dict)
        return all_drug_list

def scrap_from_web(drug_url: str):
    search_url = siteurl + drug_url
    temp_list = find_drug_basic_info(search_url)
    #print(temp_list)
    return temp_list




