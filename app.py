#Author Prasanna Hegde
#This is python file will handle the all api calls from the front end

#importing all neccessary packages
from flask import Flask,request,render_template
from flask_cors import cross_origin



app1=Flask(__name__)
ENV = 'prod'

from services import service_scrap as app_scrap

if ENV == 'dev':
    app1.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Prasanna@localhost:5432/Drug_Demo1"
    app1.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
else:
    app1.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wwndwruahmkwok:aa556b764e6c61f4b49a1514edad4ee0ef85979c253eef046f2cf498736c0d24@ec2-34-231-42-166.compute-1.amazonaws.com:5432/daklj6ji73i0ds'


#Home page url mapping
@app1.route("/",methods=['GET'])
@cross_origin()
def home():
    return render_template("index.html",search_happend="no")

@app1.route("/search_for_drug",methods=["POST"])
@cross_origin()
def search_found():
    if request.method=="POST":
        search_drug_name=request.form['drug_name'].lower()
        list_of_found_drugs=app_scrap.initial_search_scrap(search_drug_name)
        return render_template("index.html",list_of_drugs=list_of_found_drugs,search_happend="yes")



@app1.route("/find_drug",methods=['POST'])
@cross_origin()
def find_drug():
    if request.method=="POST":
        try:
            search_drug_url=request.form['drg_name']
            list_of_drugs=app_scrap.fetch_drug_list(search_drug_url)
            return render_template("show_drugs.html",list_of_drugs_model=list_of_drugs)
        except Exception as e:
            print(e)
            return render_template("error.html")

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=8001, debug=True)
	app1.run()




