# Milestone Project for Code Institute - Data Centric Development Module - By Irina Nita
This project is a Cooking Book. 

## UX
The main goal is to let users view the recipes and insert their own recipes in their cookbook.

* Main goal was to make adding recipes as user friedly as possible, this was achieved by a form with intuitive interface
* Viewing a recipe is really easy, with all the ingredients and steps displayed in a legible manner
* All significant events in the game are accompanied by alerts such as when a recipes is successfully added, deleted or edited.
* Any page is not further than 2 clicks reach

[Wireframes](https://wireframepro.mockflow.com/view/M3e2d209dde5c99a692a077a6c846a2501549016177038)
[Main Colour Palette](https://coolors.co/efd6ac-d33f49-26100a-561D25-262730)

### User Stories
1. Users that are passionate about cooking can view recipes, search based on any word.
2. Users who would like to go a step further can add their own recipes, view their own cookbook and edit or delete.
3. Users who would like to store thei recipes could add them.

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
* Add possibility for more than one image

## Technologies Used
HTML,CSS,JavaScript,Python;

[Flask](http://flask.pocoo.org/) - A microframework for Python

[MongoDB](https://www.mongodb.com/)- MongoDB is a document noSQL database

Bootstrap - For a responsive layout & prebuilt components
[Bootstrap](https://getbootstrap.com/)

Bootstrap-Select - Plugin for more complex select elements 
[Bootstrap-select] (https://developer.snapappointments.com/bootstrap-select/) 

Google Fonts - For additional fonts with particular styling
[Google fonts](https://fonts.google.com/)

Font Awesome - For icons 
[Font Awesome](https://fontawesome.com/free)

mLab - cloud database service for MongoDB databases
[mLab](https://mlab.com/company/)


## Testing

### Add Recipe Testing
1. Tested by partially filling in the input field or inserting data that would be invalid. 
    For example in the ingredients section, quantity field shouldn't allow negative values, but should allow values with decimals and hundreths
2. Submitting empty form
3. Checking that all the values already inserted were kept in the form when some information was missing


### Edit Recipe Testing


### Login/Registration Testing


## Version Control
Git and GitHub were use for version control. Commits where made at each important change, the goal was to keep them concise and relevant.


## Deployment

Deployed using Heroku


## Credits - Recipes were taken from following websites 

[1] [All Recipes](http://allrecipes.co.uk)
[2] [BBC Recipes](https://www.bbcgoodfood.com/recipes)
[3] [Jamie Oliver Recipes](https://www.jamieoliver.com/recipes/)

