#Author Prasanna Hegde.
from app import app
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy(app)

class Drug_TB(db.Model):
    __tablename__="drug_tb"
    drug_id=db.Column(db.Integer,primary_key=True)
    condition=db.Column(db.String(150))
    drug_url=db.Column(db.Text)
    drug_name=db.Column(db.Text)
    drug_label=db.Column(db.String(10))
    drug_type=db.Column(db.String(10))
    how_to_use=db.Column(db.Text)
    side_effect=db.Column(db.Text)
    rating=db.Column(db.String(10))
    image_url=db.Column(db.Text)
    image_alt=db.Column(db.Text)

# class Drug_Condition(db.Model):
#     __tablename__="drug_condition"
#     id=db.Column(db.Integer,primary_key=True)
#     condition=db.Column(db.String(100))