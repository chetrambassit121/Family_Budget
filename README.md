# Tivix-Family-Budget
Application for storing and sharing family budget information
![2022-08-29](https://user-images.githubusercontent.com/75236091/187124592-b443146f-4e31-4064-b30b-fb77088a9dc4.png)


INSTALLMENT INSTRUCTIONS:
1. Clone this repository into your local machine
2. Delete dbsqlite3, migrations, venv files/folders
3. Enter the command ... 'python -m venv venv'  ... this will create a new virtual environment in your local machine .. must be within the directory folder
4. Activate your virtual environment ... 'source venv/Scripts/activate' ... (may not need to enter source)
5. Enter the command ... 'pip install -r requirements.txt' ... this will install all the requirements needed for this project
6. Enter the command ... 'python manage.py makemigration' .. followed by .. 'python manage.py migrate' .. this will update the database with the existing models
7. Enter the command ... 'python manage.py runserver' ... this will run the local server 
8. Open browser ... go to 'localhost:8000' ... home page will be loaded!
9. Create a superuser ... 'Winpty python manage.py createsuperuser' ... You may also register a regular user.
10. All set, enjoy the web application.  

DOCKER INSTRUCTIONS:
1. Open up your local Docker Desktop application
2. enter the command ... 'docker compose up --build'
3. Tivix_Family_Budget will be pushed into the Docker containers



