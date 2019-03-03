import os
from flask import Flask,render_template,redirect,request,url_for,session,flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime
from bson.objectid import ObjectId

app=Flask(__name__)
app.secret_key = "thisaintnosecret"
app.config["MONGO_DBNAME"]="cook_book"
app.config["MONGO_URI"]="mongodb://admin:ceckbrb05@ds121295.mlab.com:21295/cook_book"

mongo=PyMongo(app)

@app.route('/', methods=['GET','POST'])
def home():
    recipes=mongo.db.recipes.find().sort('_id', -1).limit(4) #return the latest 4 recipes
    return render_template('home.html',recipes=recipes)

@app.route('/autentication', methods=['GET','POST'])
def autentication():
    message="In order to use the cook book please login"
    session['logged_in']=False
    # Release the session variable containing current user's name 
    session.pop('user', None)
    return render_template('login.html',message=message)

@app.route('/login',methods=['GET','POST'])
def login():
    users=mongo.db.users
    username=request.form['user']
    user=users.find_one({"user":username})
    password=user['password']
    if request.form['password']==password:
        session['user']=username
        session['logged_in']=True
        return redirect(url_for('home'))    
    return redirect(url_for('login.html'))

@app.route('/new_user')
def new_user():
    return render_template('new_user.html')  

@app.route('/new_user/register', methods=['GET','POST'])
def register():
    user={}
    users=mongo.db.users
    username=request.form['user']
    if users.find_one({"user":username}):
        message="User already exists, please pick another username"
        return render_template('new_user.html',message=message)
    else:    
        user["user"]=username
        user["password"]=request.form['password']
        users.insert_one(user)
        message="User created successfully"
    return render_template('login.html',message=message)  


@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    #Everytime a recipe is opened the number increases
    views=int(the_recipe['views'])
    mongo.db.recipes.update_one({'_id':ObjectId(recipe_id)},{'$inc':{'views':1}}) 
    return render_template('view_recipe.html',recipe=the_recipe,views=views)

@app.route('/recipes',defaults={'page': 1})
@app.route('/recipes/page/<page>')
def recipes(page):
    filters={}    
    if "browse" in request.args:
        filters['browse']=request.args.get("browse")
        tmpParams = [];
        tmpParams.append({"cuisine":request.args.get("browse")})
        tmpParams.append({"diet":request.args.get("browse")})
        
        if request.args.get("browse")=="All":
            findParams={}
        else:
            findParams = { '$or': tmpParams }
    else:
        findParams = {}
   
    if "keyword" in request.args and request.args.get('keyword')!="":
        keyword = request.args.get('keyword')
        mongo.db.recipes.create_index([('$**','text')])
        findParams['$text'] = { '$search': keyword  }
    else:
        keyword=None
   
    sortField = "_id"
    sortOrder = -1
    
    
    if "sort" in request.args:
        filters['sort']=request.args.get("sort")
        print(filters['sort'])
        if request.args.get('sort')=="Latest Entry First":
            sortField = '_id'
            sortOrder = -1
        elif request.args.get('sort')=="Oldest Entry First":
            sortField = '_id'
            sortOrder = 1
        elif request.args.get('sort')=="Most viewed on top":
            sortField = 'views'
            sortOrder = -1
     
    recipes_all = mongo.db.recipes.find(findParams).sort(sortField,sortOrder)
    page_size=8
    recipes_total= recipes_all.count()
   
    
    page=int(page)
    skips = page_size * (int(page) - 1)
    recipes=recipes_all.skip(skips).limit(page_size + 1)
    recipes_length=recipes.count(True)
  
   
    _diet_list=mongo.db.diet.find()
    diet_list=[diet for diet in _diet_list]
    _cuisine_list=mongo.db.cuisine.find()
    cuisine_list=[cuisine for cuisine in _cuisine_list ]
    return render_template('recipes.html',page=page,recipes=recipes,recipes_count=recipes_total,
    _diet=diet_list,_cuisine=cuisine_list,filters=filters,page_size=page_size,recipes_length=recipes_length,keyword=keyword)

@app.route('/my_recipes')
def my_recipes():
    if not session['logged_in']:
        message="In order to view your recipes or add a new one please log in"
        return render_template('login.html', message=message)
    user = session['user']    
    recipes = mongo.db.recipes.find({ 'user': user  })
    return render_template('my_recipes.html',recipes=recipes)
    
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    if not session['logged_in']:
        return redirect(url_for('autentication')) 
    mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})  
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    return redirect (url_for('my_recipes'))

"""
Editing a recipe involves minor changes applied to data that already
is in the database, such as change the quantity of a certain ingredient
or rename it more specifically, add something to an existing step. It 
does NOT allow to add new steps/ingredients as that is considered
a completely different recipe.
"""
@app.route('/edit_recipe/<recipe_id>', methods = ['GET','POST'])
def edit_recipe(recipe_id):
    if not session['logged_in']:
        return redirect(url_for('autentication'))
    user = session['user']    
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    
    #in order to avoid users editing recipes that are not theirs
    if recipe['user'] != user:
        return redirect(url_for('autentication'))
    
    _diet_list=mongo.db.diet.find()
    diet_list=[diet for diet in _diet_list]
    _cuisine_list=mongo.db.cuisine.find()
    cuisine_list=[cuisine for cuisine in _cuisine_list ]
    
    _allergens_list=mongo.db.allergens.find()
    allergens_list=[allergen for allergen in _allergens_list]
    _units=mongo.db.units.find()
    ingredient_length=len(recipe['ingredients'])
    steps_length=len(recipe['steps'])
    units_list=[unit for unit in _units]
    
   
    return render_template('edit_recipe.html',recipe=recipe,
                            _diet=diet_list,_cuisine=cuisine_list,
                            _allergens=allergens_list,units=units_list,
                            ingredient_length=ingredient_length,steps_length=steps_length)

@app.route('/update_recipe/<recipe_id>',methods=['GET','POST'])
def update_recipe(recipe_id):
    if not session['logged_in']:
        return redirect(url_for('autentication'))
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
    form_steps = request.form.getlist("steps")
  
    
    if request.form["image"]=="":
        request.form["image"]="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1024px-Good_Food_Display_-_NCI_Visuals_Online.jpg"
    
    if request.form.get('submit') == 'submit':
        recipes=mongo.db.recipes
       
        recipes.update_one({'_id': ObjectId(recipe_id)},
        {"$set":{'title':request.form['title'],
            'description':request.form['description'],
            'task_description':request.form.get('task_description'),
            'allergens':form_allergens,
            'cuisine':request.form['cuisine'],
            'diet':request.form['diet'],
            'ingredients':items,
            'steps':form_steps,
            'image':request.form['image'] }})   
    
    return redirect(url_for('my_recipes'))
    
@app.route('/add_recipe')
def add_recipe():
    if not session['logged_in']:
        message="If you would like to add a recipe please log in"
        return render_template('login.html', message=message)    
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
    return render_template('add_recipe.html',_allergens=allergens_list,
    _diet=diet_list,_cuisine=cuisine_list,units=units_list,steps=steps,
    recipes_dict=recipes_dict,ingredients=ingredients)

@app.route('/insert_recipe', methods =["POST","GET"])
def insert_recipe():
    if not session['logged_in']:
        return redirect(url_for('autentication')) 
    _units=mongo.db.units.find()
    units_list=[unit for unit in _units]
    
    _cuisine_list=mongo.db.cuisine.find()
    cuisine_list=[cuisine for cuisine in _cuisine_list ]
    
    _diet_list=mongo.db.diet.find()
    diet_list=[diet for diet in _diet_list]
    
    _allergens_list=mongo.db.allergens.find()
    allergens_list=[allergen for allergen in _allergens_list]
    
    steps = len(request.form.getlist("steps"))
  
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
    form_steps = request.form.getlist("steps")
    
    del recipes_dict["ingredient-name[]"]
    del recipes_dict["ingredient-qty[]"]
    del recipes_dict["ingredient-units[]"]
    del recipes_dict["steps"]
    
    if form_allergens:
        del recipes_dict["allergens[]"]
    recipes_dict["ingredients"]=items
    recipes_dict["steps"]=form_steps
    recipes_dict["allergens"]=form_allergens
    recipes_dict["views"]=0
    recipes_dict["user"]=session['user']
    ts=datetime.datetime.utcnow()
    recipes_dict["date"]= ts
    
    if request.form.get('submit') == 'submit':
        recipes=mongo.db.recipes
        
        if recipes_dict["image"]=="":
            recipes_dict["image"]="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1024px-Good_Food_Display_-_NCI_Visuals_Online.jpg"
            
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
    ingredients=ingredients,units=units_list,_cuisine=cuisine_list, _diet=diet_list,
    _allergens=allergens_list,form_allergens=form_allergens )    
    

if __name__=="__main__":
    app.run(host=os.environ.get('IP'),port=int(os.environ.get('PORT')),
    debug=True)
