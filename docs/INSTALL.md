## Pre-requirements

- Python 3 (recommended 3.6.2)
- PostgreSQL (9.6.5)


## Development

#### Install PostgreSQL

Recommend install PostgreSQL via docker: https://hub.docker.com/_/postgres/
~~~~
$ docker pull postgres
$ docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=yourpassword  --name postgres postgres
~~~~~

#### Install Django and dependencies
~~~~~
$ pip3 install -r requirements.txt
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
        'HOST': 'localhost',
        'PORT': '',
    }
}
~~~~~

#### Run

~~~~~
$ python3 manage.py runserver
~~~~~
The server will be available at http://127.0.0.1:8000/


## Deployment

#### Pre-requirements
- Nginx (lastest version)
- Supervisor (lastest version)
- uWsgi (lastest version)

#### Deploy
Install Python3 and PostgreSQL on your server, don't forget to install Python development library (python-dev or python-devel)

Install lastest Nginx: https://www.nginx.com/resources/admin-guide/installing-nginx-open-source/. Check `Installing From NGINX Repository
` section.

Install Supervisor:
~~~~
$ sudo apt-get install supervisor
~~~~
Install uWsgi
~~~~
$ sudo apt-get install uwsgi
OR
$ sudo pip3 install uwsgi
~~~~

Push your code to the server

Edit configuration files in conf/ to match your server settings:

- `webpyrobot.ini` is the configuration file of the project in `uwsgi`
- `webpyrobot_nginx.conf` is the  configuration file of the project in `nginx`
- `webpyrobot_uwsgi_supervisord.conf` is the configuration file to keep the project running with `uwsgi` under the management of `supervisord`

Start `supervisord` and `nginx`

~~~~
$ sudo systemctl service start supervisord
$ sudo systemctl service start nginx
~~~~


