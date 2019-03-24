# Milestone Project for Code Institute - Data Centric Development Module - By Irina Nita
---
This project is a Cooking Book, build with Python, Flask microframework and Mongo DB.
This website allows all users to view recipes. It also has a useful search and filters incroporated.
Registered users have access to their own Cooking Book where they can add/store/edit/delete their own recipes.

> Note: Varibales with an underscore used in the project `_variablename` are **NOT** private variables. They were used for
naming purposes

## UX
* The main goal was to provide a user friendly experience and an intuitive interface.
* Not registered users can view all the recipes. However, when they attempt to acces "My Cook Book"
page they will be prompted to register. As only registered users can add recipes.
* When viewing a recipe, all the inmportant information is presented in blocks, in a legible manner 
Add Recipe and Edit Recipe pages have the same structure
* All significant events on the website are accompanied by alerts such as when a recipes is successfully added, deleted or edited. 
Also when the search result was zero or when the user's Cook Book is empty.
* Any page is no further than 2 clicks reach
* When a user is loged in a "Log Out" link is displayed and viceversa
* A Disclaimer is displayed on the Login/Register pages in order to inform the users about
the fact that usernames and passwords aren't encrypted.

[Wireframes](https://wireframepro.mockflow.com/view/M3e2d209dde5c99a692a077a6c846a2501549016177038)

[Main Colour Palette](https://coolors.co/efd6ac-d33f49-26100a-561D25-262730)

### User Stories
1. Users that are passionate about cooking and are intrested only in viewing/searching for recipes, but do not intend to
add their own recipes.
2. Users who would like not only to browse and search for recipes but also to add their own recipes, view/edit/delete recipes from their own Cook Book.
3. A third category might be those who would be just interested to store their own favourite recipes, without viewing other recipes.

## Features

### Existing Features
1. Registration & login
2. View all the recipes
3. Filter and sort recipes
4. Searh through all the recipes based on a keyword
5. There is multiple select menu that allow to **exclude** recipes containing certain allergen/allergens
4. Registered users can add recipes
5. Registered users have access to their own Cook Book. Where they can view, edit and delete their own recipes
5. Recipes are added via a dynamic form, that allows to:
* add/delete ingredients/steps. 
* add a picture for each recipe
* check boxes that match allergens that the recipe contains
* choose a diet or cuisine type

### Other possible Features 

* Add more recipe categories
* Add more advanced filtering
* Add labels in recipe viewing
* Add possibility to add more than one image or provide images for each step.

## Technologies Used
HTML,CSS,JavaScript,Python;

[Flask](http://flask.pocoo.org/) - A microframework for Python

[MongoDB](https://www.mongodb.com/)- MongoDB is a document noSQL database

[Bootstrap](https://getbootstrap.com/)- For a responsive layout & prebuilt components
  
[Bootstrap-select](https://developer.snapappointments.com/bootstrap-select/)Plugin for more complex select elements 

[Google fonts](https://fonts.google.com/)- For additional fonts with particular styling

[Font Awesome](https://fontawesome.com/free) -For responsive and stylish icons

[mLab](https://mlab.com/company/)- cloud database service for MongoDB databases


## Testing

### Form Testing
* The same form structure is used for Adding and Editing Recipes. 
 Form validation that checkes whether all the field were field in is performed 
 in the backend
* Checks/restrictions like data type or step and minimum value attributes for numeric input run in the frontend.
* Tested by partially filling in the input field or inserting data that would be invalid. 
  For example in the ingredients section, quantity field shouldn't allow negative values, but should allow values with decimals and hundreths
* Submitting empty or partially empty form .
* A considerable amount of testing was dedicated to check if the input was correctly stored if for example a new step or ingredient was added
and as a result the page was refreshed.
* In the Edit section tests were made to see if, when editing, the new input was kept for the field that were edited, while all
the other fileds should maintain values from the database.

### View sort and filter recipes
* ensure that when search result is zero display an appropriate message 
* check that the results matched the filters applied
* checked that multiple selection worked correctly
* checked that the recipes that contain certain allergens were excluded as expected
* apply filters that have no result and check that an alert message is displayed

### Alert Testing
* check that after every important interaction feedback was provided via alers and user was redirected to the correct page

### Login/Registration Testing
* ensure that user couldn't access "My Recipe" section if not logged in
* check if the user that is login in is registered. That the username matches usernames in database
* If username mathces any username in database check if the password inserted matched the password from the database assocciated to the username

### View/Editing/Deleting Recipes in My Cooking Book
* ensure that user can delete/edit only his/her own recipes. For this purposes two different users where created. 
* when user has zero recipes a message should be displayed

### Next/Previous Page
* Test that when there are no recipes left the " next page" button is not displayed
* Test that when there are no previous recipes to display left the "previous page" button is not displayed

### Login/Logout
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

