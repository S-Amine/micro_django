# Micro Django 

This project provides a prototype of a cookiecutter Django template for quickly creating microservices. It uses RabbitMQ for communication, Django for backend logic, Celery for background tasks, Supervisorctl, Gunicorn, the Pika library, and Postgres. We invite you to use it and contribute.

## Features

* Custom Django command to run Rabbitmq consumer: `./manage.py rabbitmq_consume` which is persistent and attempts to reconnect if something goes wrong.
* Script for auto deployment in production: `installer.py` in a fresh Ubuntu server which the user has to input data in. The script installs OS dependencies, Python libraries in a virtualenv, installs Postgres and creates the user and the database, creates Supervisor conf files, generates .env file, and runs the processes in the background.
* Django app to interact with the Rabbitmq broker.
* File called `messages.py` to consume messages from the Rabbitmq.
* Integration for Celery that makes the import of the Celery application via the `celery_app` variable.
* Load task modules from all registered Django apps, autodiscover from `tasks.py` files inside Django apps.
* RabbitMq and Celeries settings from the Django setting file.
* Bash script called `start_celery_worker.sh` to start celery worker faster in the development stage.
* Bash script called `start_rabbitmq_consumer.sh` to start the rabbitmq message consumer quickly in the development stage.

## Getting Started

This cookiecutter template helps you set up a basic Django project with a microservices architecture. 

To get started, install the cookiecutter package:

```bash
pip install cookiecutter
```

Then, create your project:

```bash
cookiecutter https://github.com/S-Amine/micro_django.git
```

You will be asked for a few parameters, such as: 

```bash
project_name [My Awesome Project]:
```

Enter a value for `project_name` (e.g. `My Awesome Project`). 

```bash
project_slug [my_awesome_project]
```

Enter a value for `project_slug` (e.g. `my_awesome_project`) and the project will be created.

Once the project is created, navigate to the generated directory and begin the development process.

## Setting Up a Development Environment with Generated Cookiecutter Files

To get started with the project generated with this template, you need to follow these steps:

1. Create a virtual environment with the command
```bash
virtualenv env
``` 
and then activate it with 
```bash
source env/bin/activate
```
2. Create a database and a user with Postgres and store the credentials in a .env file. To do this, create the file with the command 
```bash
touch .env
``` 
or using vim
```bash
vi .env
``` 
and add the following content to it: 
```bash
DJANGO_DB_NAME=your_database_name
DJANGO_DB_USER=your_database_user
DJANGO_DB_PASSWORD=your_database_password
DJANGO_RABBITMQ_HOST=your_rabbitmq_host
DJANGO_RABBITMQ_USER=your_rabbitmq_user
DJANGO_RABBITMQ_PASSWORD=your_rabbitmq_password
```
3. Install the necessary dependencies with the command
```bash
pip install -r requirements.txt
```
4. Open 3 terminals
5. In the first terminal, activate the virtual environment and run the command 
```bash
./manage.py runserver
```
6. In the second terminal, activate the virtual environment and run the command 
```bash
./start_celery_worker.py
```
7. In the third terminal, activate the virtual environment and run the command 
```bash
./start_rabbitmq_consumer.sh
```

## How to Use the Micro Django Auto Deploy Script

Start the script by running the following command on the terminal:

```bash
python3 installer.py
```

You will then be presented with a message:

```bash
Welcome to the {{ cookiecutter.project_slug }} Auto Deploy Script

The goal of this script is to automate the installation of a microservice in an Ubuntu server.
It requires the user to specify a list of variables which includes:
 * The database name (accepts alphanumeric characters)
 * The database username (accepts alphanumeric characters)
 * The database password (accepts alphanumeric characters)
 * RabbitMQ host (accepts IP addresses and hostnames)
 * RabbitMQ user (accepts alphanumeric characters)
 * RabbitMQ password (accepts alphanumeric characters)

Do you have this information? [y/n]
```

If you answer yes, the script will prompt you for the necessary information, beginning with the database name:

```bash
Please enter the database name: 
```

The script will then ask for the database username:

```bash
Please enter the database username: 
```

Afterwards, it will prompt you to provide the database password twice to confirm it:

```bash
Please enter the database password: 
Please re-enter the database password: 
```

The script will then configure RabbitMQ by asking for the host:

```bash
Please enter the RabbitMQ host: 
```

It will then ask for the user:

```bash
Please enter the RabbitMQ user: 
```

Lastly, it will ask for the password:

```bash
Please enter the RabbitMQ password: 
Please re-enter the RabbitMQ password: 
```

Once you have provided all the required information, the script will start the installation process. 
It will update OS dependencies, install Redis, PostgreSQL, virtualenv, and Supervisor.
It will also generate the .env file and migrate the database.
Finally, it will set up Supervisor for the celery worker, rabbitmq consumer, and django app consumer, and reload Supervisor.

If there is an error at any point of the installation process, the script will stop and display the corresponding error message.

## Tech
This project uses a number of open source projects to work properly:

[Django](https://www.djangoproject.com/)
[Rabbitmq](https://www.rabbitmq.com/)
[Supervisorctl](http://supervisord.org/)
[Celery](http://www.celeryproject.org/)
[Pika](https://github.com/pika/pika)
[Postgres](https://www.postgresql.org/)
[Gunicorn](https://gunicorn.org/)

## License

<p align="center">
    <img src="https://upload.wikimedia.org/wikipedia/commons/9/93/GPLv3_Logo.svg" width="100px" height="100px">
</p>

This project is licensed under the <b>GPL3</b> license.
