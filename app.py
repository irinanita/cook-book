import os
from flask import Flask,render_template,redirect,request,url_for,session,flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import datetime
from bson.objectid import ObjectId


app=Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
app.config["MONGO_DBNAME"]="cook_book"
app.config["MONGO_URI"]=os.getenv("MONGODB_URI")

mongo=PyMongo(app)

@app.route('/')
def home():
    recipes=mongo.db.recipes.find().sort('_id', -1).limit(4) #display the latest 4 recipes
    return render_template('home.html',recipes=recipes)

@app.route('/autentication')
def autentication():
    # Release the session variables
    session.pop('logged_in', None)
    session.pop('user', None)
    return render_template('login.html')

@app.route('/setup',methods=['GET'])
def setup():
    collist=mongo.db.list_collection_names()
    if "allergens" in collist:
        print('Collection is already in the DB')
    else:
        allergens_coll=mongo.db["allergens"]
        allergens_coll.insert_one({"allergen_type": "nuts"})
        print('no')
    print(mongo.db.list_collection_names())
    return "SETUP HAPPENING HERE"

@app.route('/login',methods=['GET','POST'])
def login():
    users=mongo.db.users
    username=request.form['user']
    #Search for the inserted username in the DB
    user=users.find_one({"user":username})
    #Is user in the DB check if passwords match
    if user:
        password=user['password']
        if request.form['password']==password:
            session['user']=username
            session['logged_in']=True
            return redirect(url_for('home'))
        else:
            flash('Wrong password')    
            return redirect(url_for('autentication'))
    else:        
        flash('Wrong username')    
        return redirect(url_for('autentication'))

#Renders template for user to register
@app.route('/new_user')
def new_user():
    return render_template('new_user.html')  

#Submit registration form
@app.route('/new_user/register', methods=['GET','POST'])
def register():
    user={}
    users=mongo.db.users
    username=request.form['user']
    #Check if username already exists in DB
    if users.find_one({"user":username}):
        flash('Username already taken')
        return redirect(url_for('new_user'))
    else: 
        #Insert username and passowrd in DB and redirect to autentication page
        user["user"]=username
        user["password"]=request.form['password']
        users.insert_one(user)
        flash('User created successfully. You can now login.')
        return redirect(url_for('autentication'))
    
@app.route('/view_recipe/<recipe_id>')
def view_recipe(recipe_id):
    the_recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    #Everytime a recipe is opened the view number increases
    views=int(the_recipe['views'])
    mongo.db.recipes.update_one({'_id':ObjectId(recipe_id)},{'$inc':{'views':1}}) 
    return render_template('view_recipe.html',recipe=the_recipe,views=views)

@app.route('/recipes',defaults={'page': 1})
@app.route('/recipes/page/<page>')
def recipes(page):
    filters={}
    message=""
    #Allergens to exclude form the result
    if "exclude_allergy[]" in request.args:
        filters['exclude']=request.args.getlist('exclude_allergy[]')
        excludeParams={"allergens":{'$nin':filters['exclude']}}
    else:
        excludeParams={}
        filters['exclude']=[]
        
   #Check if user filtered by Browse(either cuisine OR diet)
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
        
    '''
    If user searched by a keyword store that 
    and display results and apply filters for that search result
    '''
    if "keyword" in request.args and request.args.get('keyword')!="":
        keyword = request.args.get('keyword')
        mongo.db.recipes.create_index([('$**','text')])
        findParams['$text'] = { '$search': keyword  }
    else:
        keyword=None
   
   #By default Sort by latest recipes
    sortField = "_id"
    sortOrder = -1
    
    #Set parameters based on Sort input
    if "sort" in request.args:
        filters['sort']=request.args.get("sort")
        if request.args.get('sort')=="Latest Entry First":
            sortField = '_id'
            sortOrder = -1
        elif request.args.get('sort')=="Oldest Entry First":
            sortField = '_id'
            sortOrder = 1
        elif request.args.get('sort')=="Most viewed on top":
            sortField = 'views'
            sortOrder = -1
            
    #Search for recipes based on the input from above
    if findParams and filters['exclude']:
        recipes_all = mongo.db.recipes.find({'$and':[findParams,excludeParams]}).sort(sortField,sortOrder)
    
    if findParams and not filters['exclude']:
        recipes_all = mongo.db.recipes.find(findParams).sort(sortField,sortOrder)
        
    if  filters['exclude'] and not findParams:
        recipes_all = mongo.db.recipes.find(excludeParams).sort(sortField,sortOrder)
    
    if not filters['exclude'] and not findParams:
        recipes_all = mongo.db.recipes.find().sort(sortField,sortOrder)
    
    page_size=8 #set how many recipes per page
    recipes_total= recipes_all.count() #display number of total recipes
    
    #If there are no recipes display the following message
    if recipes_total==0:
        message = "No recipes were found for the search criteria. Try applying different filters"
       
    page=int(page)
    skips = page_size * (int(page) - 1) #page 1 will have NO skip applied
    '''
    add 1 to see if there are any recipes left after this page
    further frontend check if recipes_length > page length, if FALSE 
    then there are no recipes after so Next Page button won't be displayed
    
    '''
    recipes=recipes_all.skip(skips).limit(page_size + 1) 
    recipes_length=recipes.count(True)
  
    #Get Diet, Cuisine and Allergens Lists from DB
    _diet_list=mongo.db.diet.find()
    diet_list=[diet for diet in _diet_list]
    _cuisine_list=mongo.db.cuisine.find()
    cuisine_list=[cuisine for cuisine in _cuisine_list ]
    _allergens_list=mongo.db.allergens.find()
    allergens_list=[allergen for allergen in _allergens_list]
    
    return render_template('recipes.html',page=page,recipes=recipes,recipes_count=recipes_total,
    _diet=diet_list,_cuisine=cuisine_list,_allergens=allergens_list,filters=filters,
    page_size=page_size,recipes_length=recipes_length,keyword=keyword,message=message)


#User can view his/her own recipes/cookbook
@app.route('/my_recipes',defaults={'page':1})
@app.route('/my_recipes/page/<page>')
def my_recipes(page):
    #If not logged in user is redirected to Autentication page
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('autentication'))
        
    #Otherwise store username in a session variable
    user = session['user']
    #Display ONLY user's recipes
    recipes_total_user= mongo.db.recipes.find({ 'user': user  }).sort('_id', -1)
    recipes_total_count=recipes_total_user.count()
    #If there are no recipes to display, how this message
    message=""
    if recipes_total_count==0:
        message="You don't have any recipes yet"
    
    #Same logic as in Recipes
    page_size=8
    page=int(page)
    skips = page_size * (int(page) - 1)
    recipes_per_page=recipes_total_user.skip(skips).limit(page_size + 1)
    recipes_length=recipes_per_page.count(True)
    
    return render_template('my_recipes.html',recipes=recipes_per_page,page_size=page_size,page=page,
            recipes_length=recipes_length,total_recipes=recipes_total_count,message=message)

#User cand delete ONLY own recipes   
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    #Check if logged in
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('autentication')) 
    '''
    Check if user from session and from recipe and from Recipe match
    if not user will be redirected to autentication. If the match is 
    True the recipe will be deleted and user redirected to his/her recipes
    '''
    user=session['user']    
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    if recipe['user'] != user:
        return redirect(url_for('autentication'))
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    flash('Your recipe was successfully deleted')
    return redirect(url_for('my_recipes'))
    

@app.route('/edit_recipe/<recipe_id>', methods = ['GET','POST'])
def edit_recipe(recipe_id):
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('autentication')) 
    user = session['user']    
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    
    #in order to avoid users editing recipes that are not theirs
    if recipe['user'] != user:
        return redirect(url_for('autentication'))
    
    #Get diet,allergens,units lists
    _diet_list=mongo.db.diet.find()
    diet_list=[diet for diet in _diet_list]
    _cuisine_list=mongo.db.cuisine.find()
    cuisine_list=[cuisine for cuisine in _cuisine_list ]
    _allergens_list=mongo.db.allergens.find()
    allergens_list=[allergen for allergen in _allergens_list]
    _units=mongo.db.units.find()
    units_list=[unit for unit in _units]
    
    ingredient_length=len(recipe['ingredients'])
    steps_length=len(recipe['steps'])
    
    return render_template('edit_recipe.html',recipe=recipe,
                            _diet=diet_list,_cuisine=cuisine_list,
                            _allergens=allergens_list,units=units_list,
                            ingredient_length=ingredient_length,steps_length=steps_length)

@app.route('/update_recipe/<recipe_id>',methods=['GET','POST'])
def update_recipe(recipe_id):
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('autentication')) 
    
    message=""
    keys_list=[] # This will be used to store the keys from empty fields
    #Get the recipe as is from DB
    recipe=mongo.db.recipes.find_one({"_id":ObjectId(recipe_id)})
    #Get all the data input from the form and transform into dictionary
    recipes_dict=request.form.to_dict()
  
    ingredient_length=len(request.form.getlist("ingredient-name[]"))
    steps_length=len(request.form.getlist("steps"))
    
    #Create an array with name, quantity and units of each ingredient
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
    
    #Get steps and allergens from the form
    form_allergens = request.form.getlist("allergens[]")
    form_steps = request.form.getlist("steps")
    
    #Delete current name,quantity and units as they are not in the format required for DB
    del recipes_dict["ingredient-name[]"]
    del recipes_dict["ingredient-qty[]"]
    del recipes_dict["ingredient-units[]"]
    del recipes_dict["steps"]
   
    #Insert data into dictionary
    recipes_dict["ingredients"]=items
    recipes_dict["steps"]=form_steps
    if form_allergens:
        del recipes_dict["allergens[]"]
        recipes_dict["allergens"]=form_allergens
    else:
        recipes_dict["allergens"]="None"
        
    if request.form.get('submit') == 'submit':
        #If no link is provided a default image is used
        if request.form["image"]=="":
            request.form["image"]="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1024px-Good_Food_Display_-_NCI_Visuals_Online.jpg"

        # To get keys which having zero length value(checks only allergens, description and title):
        keys_list = [key for key,val in recipes_dict.items() if not val]
        #Chek ingredients and steps
        keys_list_ingredients = [val for val in recipes_dict["ingredients"] if not val["units"] or not val["name"] or not val["qty"]]
        keys_list_steps = [val for val in recipes_dict["steps"] if not val]
        #If diet not in the recipes-dictionary-form
        if 'diet' not in recipes_dict:
            keys_list.append('diet')
        #If diet not in the recipes-dictionary-form    
        if 'cuisine' not in recipes_dict:
            keys_list.append('cuisine')
        #If ingredients and steps have missing values append to the array containing empy keys
        if keys_list_ingredients:
            keys_list.append('ingredients')
        if keys_list_steps:
            keys_list.append('steps')
        if keys_list:
            message="Please fill in the following data"
        else:
            recipes=mongo.db.recipes
            recipes.update_one({'_id': ObjectId(recipe_id)},{"$set":recipes_dict})  
            flash('Your recipe was successfully updated')
            return redirect(url_for('my_recipes'))
        
    elif request.form.get('submit') == 'add_step':
        steps_length += 1
    elif request.form.get('submit') == 'add_ingredient': 
        ingredient_length += 1
    elif request.form.get('submit') == 'delete_step':
        steps_length -= 1 
    elif request.form.get('submit') == 'delete_ingredient':  
        ingredient_length -= 1
    _diet_list=mongo.db.diet.find()
    diet_list=[diet for diet in _diet_list]
    _cuisine_list=mongo.db.cuisine.find()
    cuisine_list=[cuisine for cuisine in _cuisine_list ]
    _allergens_list=mongo.db.allergens.find()
    allergens_list=[allergen for allergen in _allergens_list]
    _units=mongo.db.units.find()
    units_list=[unit for unit in _units]
    
    return render_template('edit_recipe.html',recipe=recipe,recipes_dict=recipes_dict,
                            _diet=diet_list,_cuisine=cuisine_list,
                            _allergens=allergens_list,units=units_list,
                            ingredient_length=ingredient_length,steps_length=steps_length,
                            keys_list=keys_list,message=message)
    
@app.route('/add_recipe')
def add_recipe():
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('autentication')) 
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
    if session.get('logged_in') is None:
        flash("In order to use the cook book please login")
        return redirect(url_for('autentication')) 
    
    message=""
    keys_list=[] #keys of fields with no values will be stored
    
    #Units, cuisine, diet and allergens lists
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
    
    #Array of tuples with name,quantity and units for each ingredient
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
        recipes_dict["allergens"]=form_allergens
    else:
        recipes_dict["allergens"]="None"
    
    recipes_dict["ingredients"]=items
    recipes_dict["steps"]=form_steps
    recipes_dict["user"]=session['user']
  
    if request.form.get('submit') == 'submit':
        
        if recipes_dict["image"]=="":
            #if no image provided the default image is used
            recipes_dict["image"]="https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Good_Food_Display_-_NCI_Visuals_Online.jpg/1024px-Good_Food_Display_-_NCI_Visuals_Online.jpg"
        
        # To get keys which having zero length value(checks only allergens, description and title):
        keys_list = [key for key,val in recipes_dict.items() if not val]
        #Chek ingredients and steps
        keys_list_ingredients = [val for val in recipes_dict["ingredients"] if not val["units"] or not val["name"] or not val["qty"]]
        keys_list_steps = [val for val in recipes_dict["steps"] if not val]
        #If diet not in the recipes-dictionary-form
        if 'diet' not in recipes_dict:
            keys_list.append('diet')
        #If diet not in the recipes-dictionary-form    
        if 'cuisine' not in recipes_dict:
            keys_list.append('cuisine')
        #If ingredients and steps have missing values append to the array containing empy keys
        if keys_list_ingredients:
            keys_list.append('ingredients')
        if keys_list_steps:
            keys_list.append('steps')
        if keys_list:
            message="Please fill in the following data:"
        else:
            recipes_dict["views"]=0
            recipes=mongo.db.recipes
            recipes.insert_one(recipes_dict)
            flash('Your recipe was successfully added')
            return redirect(url_for('my_recipes'))
        
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
    _allergens=allergens_list,form_allergens=form_allergens,message=message,keys_list=keys_list )    
    
if __name__=="__main__":
    app.run(host=os.environ.get('IP'),port=int(os.environ.get('PORT')),
    debug=True)
