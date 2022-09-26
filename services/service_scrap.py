# Author Prasanna Hegde
# This python file will scrap the website

from services import scrap_it
from saveload import insetDrugstoDb, fetchDrugsfromDb, isAvailableInDB
import urllib.parse as parse

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
        temp_list[-1] = final_condition_name
        drug_url = "/" + "/".join(temp_list)
        #drug_dict = {}
        #drug_dict['condition'] = condition_for_db
        final_return_list=scrap_it.scrap_from_web(drug_url)
        print(final_return_list)
        #saveto db
        for dict in final_return_list:
            dict['condition'] = condition_for_db
        insert_status=insetDrugstoDb(final_return_list)
        if insert_status:
            return final_return_list
        else:
            return []



