# Milestone Project for Code Institute - Data Centric Development Module - By Irina Nita
---
This project is a Cooking Book, build with Python, Flask microframework and MongoDB.
This website allows all users to view recipes. It also has a useful search and filters incorporated.
Registered users have access to their own Cooking Book where they can add/store/edit/delete their own recipes.

> Note: Variables with an underscore used in the project `_variablename` are **NOT** private variables. They were used for
naming purposes

## UX
* The main goal was to provide a user-friendly experience and an intuitive interface.
* Not registered users can view all the recipes. However, when they attempt to access "My Cook Book"
page they will be prompted to register. As only registered users can add recipes.
* When viewing a recipe, all the important information is presented in blocks, in a legible manner 
Add Recipe and Edit Recipe pages have the same structure
* All input elements are clearly labeled, and provide placeholders and default values whenever relevant
* All significant events on the website are accompanied by alerts such as when a recipe is successfully added, deleted or edited. 
Also when the search result was zero or when the user's Cook Book is empty.
* Any page is no further than 2 clicks reach
* When a user is logged in a "Log Out" link is displayed and vice-versa
* A Disclaimer is displayed on the Login/Register pages in order to inform the users about
the fact that usernames and passwords aren't encrypted.

[Wireframes](https://wireframepro.mockflow.com/view/M3e2d209dde5c99a692a077a6c846a2501549016177038)

[Main Colour Palette](https://coolors.co/efd6ac-d33f49-26100a-561D25-262730)

### User Stories
1. Users that are passionate about cooking and are interested only in viewing/searching for recipes, but do not intend to
add their own recipes.
2. Users who would like not only to browse and search for recipes but also to add their own recipes, view/edit/delete recipes from their own Cook Book.
3. A third category might be those who would be just interested to store their own favourite recipes, without viewing other recipes.

## Features

### Existing Features
1. Registration & login
2. View all the recipes
3. Filter and sort recipes
4. Search through all the recipes based on a keyword
5. There is a multiple select menu that allows to **exclude** recipes containing certain allergen/allergens
4. Registered users can add recipes
5. Registered users have access to their own Cook Book. Where they can view, edit and delete their own recipes
5. Recipes are added via a dynamic form, that allows to:
* add/delete ingredients/steps. 
* add a picture for each recipe
* check boxes that match allergens that the recipe contains
* choose a diet or cuisine type

### Other Possible Features 

* Add more recipe categories
* Add more advanced filtering
* Add labels in recipe viewing
* Add possibility to add more than one image or provide images for each step.

## Technologies Used

### Front-end

HTML, CSS - for structure and styling purposes

[JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript) & [jQuery](https://jquery.com/) - mostly components provided by `Bootstrap` were used,
in order to create interaction like alerts that could be closed, burger button that appears on
screen resize. Navigation links that highlight when a user is at the page that matches
href

[Bootstrap](https://getbootstrap.com/) - For a responsive layout & prebuilt components
  
[Bootstrap-select](https://developer.snapappointments.com/bootstrap-select/) - Plugin for more complex select elements 

[Google fonts](https://fonts.google.com/) - For additional fonts with particular styling

[Font Awesome](https://fontawesome.com/free) - For responsive and stylish icons

### Back-end

[Python](https://www.python.org/) - Used throughout this project for the whole logic.
Python is a programming language that lets you work quickly and integrate systems more effectively

[Flask](http://flask.pocoo.org/) - A microframework for Python

[Jinja](http://jinja.pocoo.org/) - A templating language 

## Database

A non-relational `MongoDB` database was used for this project. Hence it doesn't have a rigid schema. However, the entire logic was constructed
around the `recipes collection`. Other collections such as `allergens`,`diet`,`cuisine` and `units` are complementary and contain data that
is used when a recipe is `added`; while `users` collection stores `username` and `password` of registered users, logged in user's username is
added to the `recipe document` when he\she adds a recipe. This allows us to display, in `My Cooking Book` section only those recipes that have
been added by the user that is logged in. Users can edit and delete only their own recipes.

[MongoDB](https://www.mongodb.com/) - MongoDB is a document noSQL database

[mLab](https://mlab.com/company/) - cloud database service for MongoDB databases


## Testing

### UI/UX Responsiveness Testing 
* Tested how the website adapts to different types of screen size using Chrome Dev Tools
* Navigation through website by using `go back` and `go forward` arrows to see how it reacts and to make sure 
it doesn't break
* All forms intelligently handle empty or invalid input fields

### Form Testing
* The same form structure is used for Adding and Editing Recipes. 
 Form validation that checks whether the input was provided for all the fields is performed in the backend
* Checks/restrictions like data type or step and minimum value attributes for numeric input run in the frontend.
* Tested by partially filling in the input field or inserting data that would be invalid. Clicking buttons out of the expected order or by providing unexpected inputs.
  For example in the ingredients section, quantity field shouldn't allow negative values but should allow values with decimals and hundredths
* Submitting empty or partially empty form.
* A considerable amount of testing was dedicated to checking if the input was correctly stored if for example a new step or ingredient was added
and as a result, the page was refreshed.
* In the Edit section tests were made to see if, when editing, the new input was kept for the field that was edited, while all
the other fields should maintain values from the database.

### View sort and filter recipes
* Ensure that when the search result is zero display an appropriate message 
* Check that the results matched the filters applied
* Checked that multiple selection worked correctly
* Checked that the recipes that contain certain allergens were excluded as expected
* Apply filters that have no result and check that an alert message is displayed

### Alert Testing
* Check that after every important interaction feedback was provided via alerts and user was redirected to the correct page

### Login/Registration Testing
* Ensure that user couldn't access "My Recipe" section if not logged in
* Check if the user that is login in is registered. That the username matches usernames in the database
* If username matches any username in database check if the password inserted matched the password from the database associated to the username

### View/Editing/Deleting Recipes in My Cooking Book
* Ensure that user can delete/edit only his/her own recipes. For this purposes two different users where created. 
* When a user has zero recipes a message should be displayed

### Next/Previous Page
* Test that when there are no recipes left the " next page" button is not displayed
* Test that when there are no previous recipes to display left the "previous page" button is not displayed

### Login/Logout
* Check that when a user is not logged in a "Log In" text is displayed
* Check that when a user is logged in a "Log Out" text is displayed

### Known Issues
* when clicking on an input field it sometimes becomes transparent and then reverts back


## Version Control
Git was used for version control. Commits where made at each important change, the goal was to keep them concise and relevant. All the commits war added to the remote GitHub repository

## Deployment
This Project was deployed with Heroku in the following way:
* Create Heroku account
* Login into Heroku from console `heroku login`
* Create a new empty App on Heroku as none was created before `heroku create` 
* Rename App `heroku apps: rename cook-book-project`
Run this command from App's Root. The empty Heroku Git repository is automatically set as a remote for your local repository.
Check `git remote -v`
* Create a `Procfile` (instruction to Heroku as which file should be used as an entry point for our App)
The `Procfile` must be in your app’s root directory `echo web python app.py > Procfile`
* Create a requirements.txt file `sudo pip3 freeze --local > requirements.txt`
* To deploy `git push heroku master`
* Set the `IP`,`PORT`, `SECRET_KEY` and any other environment variables in Heroku Account Settings

> When working in Flask remember to set debug to False for the deployed version

It is also possible to configure GitHub integration for a Heroku app, Heroku can automatically build and release (if the build is successful) pushes to the specified GitHub repo.
[Read more here](https://devcenter.heroku.com/articles/github-integration)

## Install Locally
* CD to the directory of your choice on your local machine and clone the repository `git clone https://github.com/irinanita/cook-book.git`
* CD into the project folder and install the dependencies `pip install -r requirements.txt`
* Set up your MongoDB database, you can leave it as it is by default with no collections.
You will need your `MongoDB URI`  
* Set your `environment variables` for `Mongo DB URI`, `Secret Key`, `Port` and `IP`. You could also store them in files that are in .gitignore.
* `App.py` contains a script that will setup a variety of collections required for this project, such as:
 `allergens_list`,`diet_list`,`cuisine_list` and `units_list`; their contents are customizable, you can add elements that you would like to see there.  
* Then open the browser and insert `localhost:PORT/setup`. This will add the collections. 
> Note that in the beginning, the landing page **won't have** recipes in the *Latest Recipes* section. They will appear as soon as you add some recipes. To do so you will need to `Register` 


## Credits - Recipes were taken from following websites 

> This Project has solely educational purpose

[1] [All Recipes](http://allrecipes.co.uk)
[2] [BBC Recipes](https://www.bbcgoodfood.com/recipes)
[3] [Jamie Oliver Recipes](https://www.jamieoliver.com/recipes/)

