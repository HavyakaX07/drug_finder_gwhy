#Author Prasanna Hegde.
from model import db,Drug_TB,Drug_Condition

def insetDrugstoDb(drugs_list:list):
    try:
        db.create_all()
        db.session.commit()
        for drug in drugs_list:
            drug_obj = Drug_TB(**drug)
            db.session.add(drug_obj)
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
def fetchDrugsfromDb(condition:str):
    try:
        final_drug_list=[]
        drug_obj=db.session.query(Drug_TB).filter(Drug_TB.condition==condition)
        for obj in drug_obj:
            temp_dict=asDict(obj)
            final_drug_list.append(temp_dict)
        return final_drug_list
    except Exception as e:
        print(e)
        return None

def isAvailableInDB(condition:str):
    try:
        db.create_all()
        db.session.commit()
        if db.session.query(Drug_Condition).filter(Drug_Condition.condition==condition).count() == 0:
            db_obj=Drug_Condition(condition=condition)
            db.session.add(db_obj)
            db.session.commit()
            return False
        else:
            return True
    except Exception as e:
        print(e)
        return False


def asDict(drug_tb):
    drug_dict={}
    drug_dict['condition']=drug_tb.condition
    drug_dict['drug_name']=drug_tb.drug_name
    drug_dict['drug_label']=drug_tb.drug_label
    drug_dict['drug_type']=drug_tb.drug_type
    drug_dict['how_to_use']=drug_tb.how_to_use
    drug_dict['side_effect']=drug_tb.side_effect
    drug_dict['rating']=drug_tb.rating
    drug_dict['image_url']=drug_tb.image_url
    drug_dict['image_alt']=drug_tb.image_alt
    return drug_dict