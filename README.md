## MaturePyRobot 2017 [![Build Status](https://travis-ci.org/AlexAndriamahaleo/MaturePyRobots.svg?branch=master)](https://travis-ci.org/AlexAndriamahaleo/MaturePyRobots)

## Pre-requirements

- Python 3 (recommended 3.6.2)
- PostgreSQL (9.6.5)
- Django (1.11.5+ recommended 1.11.6)
- Pillow: https://pillow.readthedocs.io/en/4.3.x/installation.html
Make sure you got some external libraries like zlib, libjpeg ... installed before you install Python3 if you plan to build your Python3 from source


## Development

#### Install PostgreSQL

Recommend install PostgreSQL via docker: https://hub.docker.com/_/postgres/
~~~~
$ docker pull postgres
$ docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=yourpassword  --name postgres postgres
~~~~~

#### Install dependencies and initiate data
Automate:
~~~~~
$./init.sh
~~~~~
OR manually:
~~~~~
$ pip3 install -r requirements.txt
$ python3 manage.py makemigrations
$ python3 manage.py migrate
$ python3 manage.py loaddata backend/fixtures/database.json
~~~~~

#### Configure database
- Edit  `WebPyRobot/development.py` file. Add:

~~~~
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'database_name',
        'USER': 'username',
        'PASSWORD': 'yourpostgrepassword',
        'HOST': 'db host',
        'PORT': 'db port',
    }
}
~~~~~

#### Run

~~~~
$ ./run.sh
~~~~
OR
~~~~~
$ python3 manage.py runserver
~~~~~
The server will be available at http://127.0.0.1:8000/


## Deployment

#### Pre-requirements
- Nginx (lastest version)
- Supervisor (lastest version)
- Redis

#### Deploy
Install Python3 and PostgreSQL on your server, don't forget to install Python development library (python-dev or python-devel) if you don't build Python from source

Install lastest Nginx: https://www.nginx.com/resources/admin-guide/installing-nginx-open-source/. Check `Installing From NGINX Repository
` section.

Install Supervisor:
~~~~
$ sudo apt-get install supervisor
~~~~
Install redis
~~~~
$ sudo apt-get install redis-server
~~~~

Push your code to the server

Edit WebPyRobot/production.py to add your database, secret key, Channels settings for production

Install dependencies and initiate data:
~~~~
$ ./init.sh
~~~~
Setup static files for Nginx
~~~~
$ python3 prod_manage.py collectstatic
~~~~
Edit configuration files in conf/ to match your server settings:

- `webpyrobot_channels_supervisord.conf` is the configuration file to keep the project running with `daphne` under the management of `supervisord`. It's also for managing Channels workers
- `webpyrobot_nginx.conf` is the  configuration file of the project in `nginx`

Start `supervisord` and `nginx`

~~~~
$ sudo systemctl service start supervisord
$ sudo systemctl service start nginx
~~~~

Enjoy your production!

