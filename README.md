# Milestone Project for Code Institute - Data Centric Development Module - By Irina Nita
This project is a Cooking Book. 

## UX
The main goal is to let users view the recipes and insert their own recipes in their cookbook.

* Main challenge was to make the process of adding/editing recipes as user friedly as possible, this was achieved by a form with intuitive interface
* Viewing a recipe, all the inmportant information is presented in blocks, in a legible manner 
Add Recipe and Edit Recipe pages have the same structure
* All significant events on the website are accompanied by alerts such as when a recipes is successfully added, deleted or edited.
* Any page is not further than 2 clicks reach

[Wireframes](https://wireframepro.mockflow.com/view/M3e2d209dde5c99a692a077a6c846a2501549016177038)
[Main Colour Palette](https://coolors.co/efd6ac-d33f49-26100a-561D25-262730)

### User Stories
1. Users that are passionate about cooking can view recipes, search for a recipe based on any word. Filter and sort them for a more relevant result.
2. Users who would like to go a step further can add their own recipes, view their own cookbook and edit or delete.

## Features

### Existing Features
1. Registration & login
2. View all the recipes
3. Filter and sort recipes
4. Registered users can add recipes
5. Recipes are added via form, where it is possible to dynamically add/remove ingredients/steps
5. Registered users can view, edit and delete their own recipes
6. Editing recipes occurs via the same form as adding them

### Other possible Features 

* Add more recipe categories
* Add more advanced filtering
* Add labels in recipe viewing
* Add possibility to add more than one image or provide images for each step.

## Technologies Used
HTML,CSS,JavaScript,Python;

[Flask](http://flask.pocoo.org/) - A microframework for Python

[MongoDB](https://www.mongodb.com/)- MongoDB is a document noSQL database

Bootstrap - For a responsive layout & prebuilt components
[Bootstrap](https://getbootstrap.com/)

Bootstrap-Select - Plugin for more complex select elements 
[Bootstrap-select](https://developer.snapappointments.com/bootstrap-select/) 

Google Fonts - For additional fonts with particular styling
[Google fonts](https://fonts.google.com/)

Font Awesome - For icons 
[Font Awesome](https://fontawesome.com/free)

mLab - cloud database service for MongoDB databases
[mLab](https://mlab.com/company/)


## Testing

### Form Testing
* The same form structure is used for Adding and Editing Recipes. 
 Form validation that checkes whether all the field were field in is performed 
 in the backend. However, restrictions like data type or step and minimum value 
 attributes for numeric input run in the frontend.
** Tested by partially filling in the input field or inserting data that would be invalid. 
    For example in the ingredients section, quantity field shouldn't allow negative values, but should allow values with decimals and hundreths
** Submitting empty form or partially empty.

* A considerable amount of testing was dedicated to check if the input was stored if for example a new step or ingredient was added
and as a result the page was refreshed.

* In the Edit section tests were made to see if, when editing, the new input was kept for the field that were edited, while all
the other fileds should maintain values from the database.

### View sort and filer recipes
* check that the results matched the filters applied
* checked that multiple selection worked correctly
* checked that the recipes that contain certain allergens were excluded as expected

### Alert Testing
* check that after every important interaction feedback was provided via alers and user was redirected to the correct page

### Login/Registration Testing
* ensure that user couldn't access "My Recipe" section if not logged in
* check if the user that is login in is registered. That the username matches usernames in database
* If username mathces any username in database check if the password inserted matched the password from the database assocciated to the username

### View/Editing/Deleting Recipes in My Recipes
* ensure that user can delete/edit only his/her own recipes

### Next/Previous Page
* Test that when there are no recipes left the " next page" button is not displayed
* Test that when there are no previous recipes to display left the "previous page" button is not displayed

###Login/Logout
* check that when a user is not loged in a "Log In" text is displayed
* check that when a user is loged in a "Log Out" text is displayed

## Version Control
Git and GitHub were use for version control. Commits where made at each important change, the goal was to keep them concise and relevant.

## Deployment

Deployed using Heroku


## Credits - Recipes were taken from following websites 

[1] [All Recipes](http://allrecipes.co.uk)
[2] [BBC Recipes](https://www.bbcgoodfood.com/recipes)
[3] [Jamie Oliver Recipes](https://www.jamieoliver.com/recipes/)

