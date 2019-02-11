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
    _diet_list=mongo.db.diet.find()
    diet_list=[diet for diet in _diet_list]
    _cuisine_list=mongo.db.cuisine.find()
    cuisine_list=[cuisine for cuisine in _cuisine_list ]
    _units=mongo.db.units.find()
    units_list=[unit for unit in _units]
    steps = 2
    ingredients=2
    recipes_dict={}
    form_steps=[]
    return render_template('add_recipe.html',_allergens=allergens_list,
    _diet=diet_list,_cuisine=cuisine_list,units=units_list,steps=steps,recipes_dict=recipes_dict,ingredients=ingredients)

@app.route('/insert_recipe', methods =["POST","GET"])
def insert_recipe():
    _units=mongo.db.units.find()
    units_list=[unit for unit in _units]
    
    _cuisine_list=mongo.db.cuisine.find()
    cuisine_list=[cuisine for cuisine in _cuisine_list ]
    
    _diet_list=mongo.db.diet.find()
    diet_list=[diet for diet in _diet_list]
    
    _allergens_list=mongo.db.allergens.find()
    allergens_list=[allergen for allergen in _allergens_list]
    
    steps = len(request.form.getlist("steps"))
    print('steps',steps)
   
    ingredientsList = request.form.getlist("ingredient-name[]")
    ingredients = len(ingredientsList)
    
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
    
    
    form_allergens = request.form.getlist("allergens[]")
    
    print('form_allergens',form_allergens)
    
    form_steps = request.form.getlist("steps")
    form_diet = request.form['diet']
    del recipes_dict["ingredient-name[]"]
    del recipes_dict["ingredient-qty[]"]
    del recipes_dict["ingredient-units[]"]
    del recipes_dict["steps"]
    if form_allergens:
        del recipes_dict["allergens[]"]
    recipes_dict["ingredients"]=items
    recipes_dict["steps"]=form_steps
    recipes_dict["allergens"]=form_allergens
    
    if request.form.get('submit') == 'submit':
        recipes=mongo.db.recipes
        recipes.insert_one(recipes_dict)
        
    elif request.form.get('submit') == 'add_step':
        # add step
        steps += 1
    elif request.form.get('submit') == 'add_ingredient': 
        ingredients += 1
    elif request.form.get('submit') == 'delete_step':
        steps -= 1 
    elif request.form.get('submit') == 'delete_ingredient':  
        ingredients -= 1
 
    return render_template('add_recipe.html', steps=steps, form_steps=form_steps, recipes_dict=recipes_dict,
    ingredients=ingredients,selected_diet=form_diet,units=units_list,_cuisine=cuisine_list, _diet=diet_list,
    _allergens=allergens_list,form_allergens=form_allergens )    
    

if __name__=="__main__":
    app.run(host=os.environ.get('IP'),port=int(os.environ.get('PORT')),
    debug=True)
