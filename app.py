import os
from flask import Flask,render_template,redirect,request,url_for
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

@app.route('/insert_recipe', methods =["POST","GET"])
def insert_recipe():
    recipes=mongo.db.recipes
    recipes_dict=request.form.to_dict()
    headers = ('name', 'qty','units')
    values = (
        request.form.getlist('ingredient-name[]'),
        request.form.getlist('ingredient-qty[]'),
        request.form.getlist('ingredient-units[]'),
    )
    items = [{} for i in range(len(values[0]))]
    for x,i in enumerate(values):
        for _x,_i in enumerate(i):
            items[_x][headers[x]] = _i
    
    form_allergens = request.form.getlist("allergens")
    form_steps = request.form.getlist("steps")
    print(form_steps)
    del recipes_dict["ingredient-name[]"]
    del recipes_dict["ingredient-qty[]"]
    del recipes_dict["ingredient-units[]"]
    del recipes_dict["steps"]
    recipes_dict["ingredients"]=items
    recipes_dict["allergens"]=form_allergens
    recipes_dict["steps"]=form_steps
    recipes.insert_one(recipes_dict)
    return render_template('add_recipe.html')    


if __name__=="__main__":
    app.run(host=os.environ.get('IP'),port=int(os.environ.get('PORT')),
    debug=True)
