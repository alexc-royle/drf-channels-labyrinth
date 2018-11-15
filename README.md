# Labyrinth App using django, drf, channels and react
This project builds upon previous work done in django and react, bringing them both together. This project uses docker-compose to run everything

## Getting started
### Prerequisites
### Installing
## Running Tests
### End to end Tests
### Coding style Tests
## Deployment
## Built with
## Authors
## Acknowledgements

## Helpful instructions
* Creating a django project `sudo docker-compose run web django-admin.py startproject <project_name> .`
* Creating an app `docker-compose run web python3 manage.py startapp <app_name>`
* Start the project `docker-compose up`
* Close the project `docker-compose down`
* Create migrations `docker-compose run web python3 manage.py makemigrations <app_name>`
* Migrate any changes `docker-compose run web python3 manage.py migrate`
* Change file/folder ownership `sudo chown -R  $USER:$USER .`
* Run django shell `docker-compose run web python3 manage.py shell`
* Create superuser for admin `docker-compose run web python3 manage.py createsuperuser`
