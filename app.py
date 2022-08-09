from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms_sqlalchemy.fields import QuerySelectField
#import random

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///asset.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Asset(db.Model):
    Name=db.Column(db.String(length=30))
    Asset_ID=db.Column(db.Integer(),primary_key=True)
    Classification=db.Column(db.String(length=30))
    Type=db.Column(db.String(length=30))
    Category=db.Column(db.String(length=30))
    

    def __repr__(self) ->str:
        return f'Asset {self.Name} - {self.Asset_ID}'


 
@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/assets", methods=['GET','POST'])
def assets():
    
    if request.method=='POST' :
        Name=request.form['Name']
        Classification=request.form['Classification']
        Category=request.form['Category']
        Type=request.form['Type']
        Asset_ID=request.form.get('Asset_ID')
        
        '''if Category is not None :       
            workout = Asset(Category=Category)
            db.session.add(workout)
            db.session.commit() 
            # you can redirect to home page on successful commit. or anywhere else
            return redirect(url_for('assets'))       
        else:
            error="Error, your log is incomplete! Please check and submit it again!"'''


        
        asset=Asset(Name=Name,Asset_ID=Asset_ID,Classification=Classification,Category=Category,Type=Type)
        db.session.add(asset)
        db.session.commit()
    assets=Asset.query.all()
    
    return render_template("assets.html",assets=assets)

@app.route("/newAsset", methods=['GET','POST'])
def new_asset():
    #Asset_ID=random.randint(100000,999999) 
    if request.method=='POST':
        Name=request.form['Name']
        Classification=request.form['Classification']
        Category=request.form['Category']
        Type=request.form['Type']
        
        asset=Asset(Name=Name,Classification=Classification,Category=Category,Type=Type)
        db.session.add(asset)
        db.session.commit()
    
        
    Types = ['Laptop', 'Mobile', 'Others']
    allAssets=Asset.query.all()
    
    return render_template("add_asset.html",assets=assets,Types=Types)

@app.route("/update/<int:Asset_ID>",methods=['GET','POST'])
def update(Asset_ID):
    if request.method=='POST':
        asset=Asset.query.filter_by(Asset_ID=Asset_ID).first()
        Name=request.form['Name']
        Classification=request.form['Classification']
        Category=request.form['Category']
        Type=request.form['Type']
        
        asset.Name=Name
        asset.Classification=Classification
        asset.Category=Category
        asset.Type=Type
        db.session.add(asset)
        db.session.commit()
        return redirect("/assets")
    Types = ['Laptop', 'Mobile', 'Others']
    asset=Asset.query.filter_by(Asset_ID=Asset_ID).first()
    return render_template('update.html',asset=asset,Types=Types)

@app.route("/delete/<int:Asset_ID>")
def delete(Asset_ID):
    asset=Asset.query.filter_by(Asset_ID=Asset_ID).first()
    db.session.delete(asset)
    db.session.commit()
    return redirect("/assets")


if __name__=="__main__":
    app.run(debug=True)
