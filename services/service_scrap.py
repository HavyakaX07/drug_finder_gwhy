# Author Prasanna Hegde
# This python file will scrap the website

from services import scrap_it
from saveload import insetDrugstoDb, fetchDrugsfromDb, isAvailableInDB, save_image_details_inDB,fetch_image_url_from_db, is_image_availableInDB
import urllib.parse as parse

from services.image_scrapit import fetch_drug_image

final_condition_name=""
condition_for_db=""


def initial_search_scrap(drug_name: str):
    drug_name_list=drug_name.split(" ")
    if(drug_name_list[-1]==""):
        del drug_name_list[-1]
    global final_condition_name
    final_condition_name="%20".join(drug_name_list)
    initial_search_final_condition_name=parse.quote(drug_name)
    search_url = "https://www.webmd.com/drugs/2/search?type=conditions&query=" + initial_search_final_condition_name
    return scrap_it.initial_search(search_url)


def fetch_drug_list(drug_url: str):
    dummy_list=drug_url.split("/")
    condition_for_db=dummy_list[-1]
    status=isAvailableInDB(condition_for_db)
    print("is available ",status)
    if status:
        return fetchDrugsfromDb(condition_for_db)
    else:
        temp_list = drug_url.split("/")
        del temp_list[0]
        temp_list[-1] = condition_for_db
        drug_url = "/" + "/".join(temp_list)
        drug_dict = {}
        drug_dict['condition'] = condition_for_db
        print(drug_url)
        final_return_list=scrap_it.scrap_from_web(drug_url)
        print(f"final_return_list for only web scrap is {final_return_list}")
        if(len(final_return_list)!=0):
            # saveto db
            for dict in final_return_list:
                dict['condition'] = condition_for_db
            insert_status = insetDrugstoDb(final_return_list)
            if insert_status:
                return final_return_list
            else:
                return []
        else:
            return []

def fetch_drug_image_service(drug_url:str):
    is_imagePresent=is_image_availableInDB(drug_url)
    if is_imagePresent:
        image_dict=fetch_image_url_from_db(drug_url)
        if image_dict['image_url'] != "None":
            image_url_list = image_dict['image_url'].split("<!sep!hegde!>")
            image_alt_list = image_dict['image_alt'].split("<!sep!hegde!>")
            final_return_list=[(image_url_list[i],image_alt_list[i]) for i in range(len(image_url_list))]
            print(final_return_list)
            return final_return_list
        else:
            return []

    else:
        image_dict=fetch_drug_image(drug_url)
        save_image_details_inDB(drug_url,image_dict)
        if image_dict['image_url'] != "None":
            image_url_list = image_dict['image_url'].split("<!sep!hegde!>")
            image_alt_list = image_dict['image_alt'].split("<!sep!hegde!>")
            final_return_list = [(image_url_list[i], image_alt_list[i]) for i in range(len(image_url_list))]
            print(final_return_list)
            return final_return_list
        else:
            return []





