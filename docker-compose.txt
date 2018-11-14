# Create django project
sudo docker-compose run web django-admin.py startproject learning_site .

# start the project
docker-compose up

# close the project
docker-compose down

# run migrate
docker-compose run web python3 manage.py migrate

# create an app
docker-compose run web python3 manage.py startapp courses

# change file/folder ownership to current user in current directory
sudo chown -R  $USER:$USER .

# run makemigrations after changes to models etc. Need to run migrate after this
docker-compose run web python3 manage.py makemigrations <name_of_app>

# run django shell
docker-compose run web python3 manage.py shell

# create superuser for/admin
docker-compose run web python3 manage.py createsuperuser
