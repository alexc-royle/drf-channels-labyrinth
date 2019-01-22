# Labyrinth App using django, drf, channels and react
This project builds upon previous work done in django and react, bringing them both together. This project uses docker-compose to run everything

## API
* game:
** get - list all games
** post - create a game
** put - n/a
** delete - n/a
* game/pk:
** get - get game details
** put - edit game details
** delete - delete a game
** create - n/a
* game/pk/pieces
** get - list game pieces per game
** post - n/a
** push - n/a
** delete - n/a
* game/pk/collectables
** get - list collectables per game
** post - n/a
** push - n/a
** delete - n/a
* game/pk/players
** get - list players in game
** post - add a player to a game
** delete - n/a
** push - n/a
* game/pk/playercounters
** get - get all player counters
** post - n/a
** put - n/a
** delete - n/a
* game/pk/rotatesparesquare
** post - rotate the spare square, returns the updated spare square
** get - n/a
** put - n/a
** delete - n/a
* game/pk/insertsparesquare
** post - inserts the spare square. returns the updated pieces
** get - n/a
** put - n/a
** delete - n/a
* game/pk/movecounter
** post - moves the counter of the current player. returns all the playercounters
** get - n/a
** put - n/a
** delete - n/a
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
