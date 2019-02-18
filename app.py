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
def login():
    message="In order to use the cook book please login"
    session['logged_in']=False
    return render_template('login.html',message=message)

@app.route('/login',methods=['GET','POST'])
def login_2():
    users=mongo.db.users
    username=request.form['user']
    user=users.find_one({"user":username})
    password=user['password']
    if request.form['password']==password:
        session['user']=username
        session['logged_in']=True
        return redirect(url_for('home'))    
    return render_template('login.html')

@app.route('/new_user')
def new_user():
    return render_template('new_user.html')  

@app.route('/new_user/register', methods=['GET','POST'])
def register():
    user={}
    users=mongo.db.users
    username=request.form['user']
    if users.find_one({"user":username}):
        print('existing user, pick another username')
        message="User already exists, please pick another username"
        return render_template('new_user.html',message=message)
    else:    
        user["user"]=username
        user["password"]=request.form['password']
        users.insert_one(user)
        print(user,'created')
        message="User created successfully"
    return render_template('login.html',message=message)  

    

@app.route('/home')
def home():
    if not session['logged_in']:
        return redirect(url_for('login'))    
    recipes=mongo.db.recipes.find().sort('_id', -1).limit(4) #return the latest 4 recipes
    return render_template('home.html',recipes=recipes)
  
        

@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    if not session['logged_in']:
        return redirect(url_for('login')) 
    the_recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    views=int(the_recipe['views'])
    mongo.db.recipes.update_one({'_id':ObjectId(recipe_id)},{'$inc':{'views':1}})
    return render_template('view_recipe.html',recipe=the_recipe,views=views)

@app.route('/recipes',methods =["POST","GET"])
def recipes():
    if not session['logged_in']:
        return redirect(url_for('login')) 
    if "browse" in request.form:
        tmpParams = [];
        tmpParams.append({"cuisine":request.form["browse"]})
        tmpParams.append({"diet":request.form["browse"]})
        
        if request.form["browse"]=="All":
            findParams={}
        else:
            findParams = { '$or': tmpParams }
    else:
        findParams = {}
   
    if "keyword" in request.args:
        keyword = request.args.get('keyword')
        mongo.db.recipes.create_index([('$**','text')])
        findParams['$text'] = { '$search': keyword  }
   
    sortField = "_id"
    sortOrder = -1
    
    if "sort" in request.form:
        if request.form['sort']=="Latest Entry First":
            sortField = '_id'
            sortOrder = -1
        elif request.form['sort']=="Oldest Entry First":
            sortField = '_id'
            sortOrder = 1
        elif request.form['sort']=="Most viewed on top":
            sortField = 'views'
            sortOrder = -1
    
    recipes = mongo.db.recipes.find(findParams).sort(sortField,sortOrder)
    
    _diet_list=mongo.db.diet.find()
    diet_list=[diet for diet in _diet_list]
    _cuisine_list=mongo.db.cuisine.find()
    cuisine_list=[cuisine for cuisine in _cuisine_list ]
    return render_template('recipes.html',recipes=recipes,_diet=diet_list,_cuisine=cuisine_list)

    
@app.route('/add_recipe')
def add_recipe():
    if not session['logged_in']:
        return redirect(url_for('login')) 
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
        return redirect(url_for('login')) 
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
    ingredients=ingredients,selected_diet=form_diet,units=units_list,_cuisine=cuisine_list, _diet=diet_list,
    _allergens=allergens_list,form_allergens=form_allergens )    
    

if __name__=="__main__":
    app.run(host=os.environ.get('IP'),port=int(os.environ.get('PORT')),
    debug=True)
