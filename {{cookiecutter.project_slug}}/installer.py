# This script will help automate the installation process of the micro service in Ubuntu server
from install_utils import (update_os,
                   install_redis,
                   install_postgres,
                   install_virtualenv,
                   install_supervisor,
                   create_supervisor_config,
                   project_name,
                   reload_supervisor,
                   verify_input,
                   is_host_or_ip,
                   verify_password,
                   generate_env,
                   migrate
                   )
import getpass
import re

answer = None

colors = {
    "yellow": "\033[1;33m",
    "green": "\033[1;32m",
    "cyan": "\033[1;36m",
    "red": "\033[1;31m"
}

print(f"""
{colors['cyan']}
Welcome to the {{cookiecutter.project_slug}} Auto Deploy Script

The goal of this script is to automate the installation of a microservice in an Ubuntu server.
It requires the user to specify a list of variables which includes:
 * The database name (accepts alphanumeric characters)
 * The database username (accepts alphanumeric characters)
 * The database password (accepts alphanumeric characters)
 * RabbitMQ host (accepts IP addresses and hostnames)
 * RabbitMQ user (accepts alphanumeric characters)
 * RabbitMQ password (accepts alphanumeric characters)

\033[0m""")

while answer not in ("y", "n"):
    answer = input(f"{colors['red']}\nDo you have these informations ? [y/n] : \033[0m")
    if answer.lower() == "y":

        # Get the database name
        db_name = verify_input("\nPlease enter the database name: ")

        # Get the database username
        db_user = verify_input("\nPlease enter the database username: ")

        # Get the database password and make sure it matches
        db_pass = verify_password("\nPlease enter the database password: ")

        # Now let's configure RabbitMQ
        print(f"{colors['yellow']}\nNow let's configure RabbitMQ...\033[0m")

        # Get the RabbitMQ host
        rabbitmq_host = is_host_or_ip("\nPlease enter the RabbitMQ host: ")

        # Get the RabbitMQ user
        rabbitmq_user = verify_input("\nPlease enter the RabbitMQ user: ")

        # Get the RabbitMQ password and make sure it matches
        rabbitmq_pass = verify_password("\nPlease enter the RabbitMQ password: ")

        print(f"{colors['green']}\nThank you for providing the necessary informations. The installation process will start, but please provide your sudo password before continuing...\033[0m")

        # Start the installation process

        # 1 Update Os dependencies
        try:
            print(f"{colors['cyan']}\nUpdating OS dependencies...\033[0m")
            update_os()
            print(f"{colors['green']}\nSuccessfully updated OS dependencies!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while updating OS dependencies: {e}\033[0m")
            exit()

        # 2 Install Redis
        try:
            print(f"{colors['cyan']}\nInstalling Redis...\033[0m")
            install_redis()
            print(f"{colors['green']}\nSuccessfully installed Redis!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while installing Redis: {e}\033[0m")
            exit()

        # 3 Install PostgreSQL
        try:
            print(f"{colors['cyan']}\nInstalling PostgreSQL...\033[0m")
            install_postgres(username=db_user, password=db_pass, dbname=db_name)
            print(f"{colors['green']}\nSuccessfully installed PostgreSQL!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while installing PostgreSQL: {e}\033[0m")
            exit()

        # 4 Install & set the virtualenv
        try:
            print(f"{colors['cyan']}\nInstalling and setting up virtualenv...\033[0m")
            install_virtualenv()
            print(f"{colors['green']}\nSuccessfully installed and set up virtualenv!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while installing and setting up virtualenv: {e}\033[0m")
            exit()

        # 5 Generate the .env file
        try:
            print(f"{colors['cyan']}\nGenerating .env file...\033[0m")
            generate_env(django_db_name=db_name,
                         django_db_user=db_user,
                         django_db_password=db_pass,
                         django_rabbitmq_host=rabbitmq_host,
                         django_rabbitmq_user=rabbitmq_user,
                         django_rabbitmq_password=rabbitmq_pass
                         )
            print(f"{colors['green']}\nSuccessfully generated .env file!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while generating .env file: {e}\033[0m")
            exit()
        # 6 migrate the database
        try:
            print(f"{colors['cyan']}\nMigrating the database...\033[0m")
            migrate()
            print(f"{colors['green']}\nSuccessfully migrated the database!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while migrating the database: {e}\033[0m")
            exit()

        # 7 Install Supervisor
        try:
            print(f"{colors['cyan']}\nInstalling Supervisor...\033[0m")
            install_supervisor()
            print(f"{colors['green']}\nSuccessfully installed Supervisor!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while installing Supervisor: {e}\033[0m")
            exit()

        # 8 Supervisor setup for celery worker
        try:
            print(f"{colors['cyan']}\nSetting up Supervisor for celery worker...\033[0m")
            create_supervisor_config(f'{project_name}_celery_worker',
                                     f'env/bin/celery -A {project_name}.celery worker --loglevel=info',
                                     '/tmp/celery_worker.conf')
            print(f"{colors['green']}\nSuccessfully set up Supervisor for celery worker!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while setting up Supervisor for celery worker: {e}\033[0m")
            exit()

        # 9 Supervisor setup for rabbitmq consumer
        try:
            print(f"{colors['cyan']}\nSetting up Supervisor for rabbitmq consumer...\033[0m")
            create_supervisor_config(f'{project_name}_rabbitmq_consumer',
                                     'env/bin/python3 manage.py rabbitmq_consume',
                                     '/tmp/rabbitmq_consumer.conf')
            print(f"{colors['green']}\nSuccessfully set up Supervisor for rabbitmq consumer!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while setting up Supervisor for rabbitmq consumer: {e}\033[0m")
            exit()

        # 10 Supervisor setup for django app consumer
        try:
            print(f"{colors['cyan']}\nSetting up Supervisor for django app consumer...\033[0m")
            create_supervisor_config(f'{project_name}_django_app',
                                     f'env/bin/gunicorn {project_name}.wsgi:application',
                                     '/tmp/django_app.conf')
            print(f"{colors['green']}\nSuccessfully set up Supervisor for django app consumer!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while setting up Supervisor for django app consumer: {e}\033[0m")
            exit()

        # 11 Reload supervisor
        try:
            print(f"{colors['cyan']}\nReloading Supervisor...\033[0m")
            reload_supervisor()
            print(f"{colors['green']}\nSuccessfully reloaded Supervisor!\033[0m")
        except Exception as e:
            print(f"{colors['red']}\nError while reloading Supervisor: {e}\033[0m")
            exit()

    elif answer.lower() == "n":
        break
    else:
        print(f"{colors['yellow']}\nPlease enter y or n.\033[0m")
