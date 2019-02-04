import os
from flask import Flask,render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app=Flask(__name__)
app.config["MONGO_DBNAME"]="cook_book"
app.config["MONGO_URI"]="mongodb://admin:ceckbrb05@ds121295.mlab.com:21295/cook_book"

mongo=PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_recipe')
def add_recipe():
    allergens_list=mongo.db.allergens.find()
    diet_list=mongo.db.diet.find()
    cuisine_list=mongo.db.cuisine.find()
    _units=mongo.db.units.find()
    units_list=[unit for unit in _units]
    return render_template('add_recipe.html',_allergens=allergens_list,
    _diet=diet_list,_cuisine=cuisine_list,units=units_list)



if __name__=="__main__":
    app.run(host=os.environ.get('IP'),port=int(os.environ.get('PORT')),
    debug=True)
