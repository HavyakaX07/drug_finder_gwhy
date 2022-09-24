#Author Prasanna Hegde
#This is python file will handle the all api calls from the front end

#importing all neccessary packages
from flask import Flask,request,render_template
from flask_cors import cross_origin



app=Flask(__name__)
ENV = 'prod'

from services import service_scrap as app_scrap

if ENV == 'dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:Prasanna@localhost:5432/Drug_Demo1"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://tqvbnkhljhoanv:0fe24a668ffc3741a5f21990cfd6d7c823d78dfee52d3e76de041cce677a2657@ec2-18-214-35-70.compute-1.amazonaws.com:5432/d68dtj97quva3m'
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
        search_drug_name=request.form['drug_name'].lower()
        list_of_found_drugs=app_scrap.initial_search_scrap(search_drug_name)
        return render_template("index.html",list_of_drugs=list_of_found_drugs,search_happend="yes")



@app.route("/find_drug",methods=['POST'])
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
	app.run()




