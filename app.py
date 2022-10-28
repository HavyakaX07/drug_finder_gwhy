#Author Prasanna Hegde
#This is python file will handle the all api calls from the front end

#importing all neccessary packages
from flask import Flask,request,render_template
from flask_cors import cross_origin
list_of_drugs=[]


app=Flask(__name__)
ENV = 'Prod'


from services import service_scrap as app_scrap



if ENV == 'Dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Prasanna@localhost:5432/Drug_Demo1"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = '##** secret **##'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#Home page url mapping
@app.route("/",methods=['GET'])
@cross_origin()
def home():
    return render_template("index.html",search_happend="no")

@app.route("/search_for_drug",methods=["POST"])
@cross_origin()
def search_found():
    if request.method=="POST":
        print("Requested method is post")
        search_drug_name=request.form['drug_name'].lower()
        list_of_found_drugs=app_scrap.initial_search_scrap(search_drug_name)
        return render_template("index.html", list_of_drugs=list_of_found_drugs, search_happend="yes")



@app.route("/find_drug",methods=['POST'])
@cross_origin()
def find_drug():
    if request.method=="POST":
        try:
            search_drug_url=request.form['drg_name']
            global list_of_drugs
            list_of_drugs = app_scrap.fetch_drug_list(search_drug_url)
            print(f"LIst of Drugs {list_of_drugs}")
            return render_template("show_drugs.html", list_of_drugs_model=list_of_drugs,drug_image={})
        except Exception as e:
            print(e)
            return render_template("error.html")
@app.route("/view_image",methods=["POST"])
@cross_origin()
def fetch_image():
    if request.method=="POST":
        try:
            drug_url=request.form['drug_url']
            image_dict=app_scrap.fetch_drug_image_service(drug_url)
            return render_template('show_drug_image.html',drug_image=image_dict)
        except Exception as e:
            print(e)
            return render_template('show_drug_image.html',drug_image=[])



if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=8001)
    app.run()




