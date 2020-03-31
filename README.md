# Getting started with "What's New On Wiki?"
The list of operations to do in order to start the web service is enumerated below:

### Set up the database MySQL
1. Make sure that a MySQL server is running on localhost
2. Create a user named "wnow" with password "2020" 
3. Create a new database named "wnow"
4. In a new terminal, open the directory "wnow_site"
5. Type "php artisan migrate"; this command will set up the database

### Start the Python script
6. In a new terminal, open the directory "app"
7. Run the script "recommender_engine.py"

### Start Laravel server
8. In a new terminal, open the directory "wnow_site"
9. Type "php artisan serve"
10. Open the browser and type "localhost:8000"

