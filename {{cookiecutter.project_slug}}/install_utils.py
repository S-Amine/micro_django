# This script will help automate the installation process of the micro service in Ubuntu server

import os
import getpass
import subprocess
import re

# Get current user
user_name = getpass.getuser()

# Get current repo
project_dir = os.getcwd()
project_name = os.path.basename(project_dir)

# Update the apt packages
def update_os():
    # Install Redis packages
    os.system("sudo apt-get update -y")

# Install Redis
def install_redis():
    """
    Installs and configures Redis on the system.
    """

    # Install Redis packages
    os.system("sudo apt-get install redis-server")

    # Verify the installation
    if subprocess.call(["redis-cli", "ping"]) == 0:
        # Start the Redis service
        os.system("sudo systemctl start redis-server")

        # Enable Redis to start on boot
        os.system("sudo systemctl enable redis-server")

        # Print a success message
        print("Redis installation completed successfully!")
    else:
        print("Redis installation failed!")

# Install and configure PostgreSQL
def install_postgres(username, password, dbname):
    """
    Installs PostgreSQL and configures it with the given username and password.
    """

    # Install PostgreSQL
    result = subprocess.call(["sudo", "apt-get", "install", "postgresql", "-y"])
    if result != 0:
        print("Installation failed!")
        return

    # Create new user and database
    subprocess.run('sudo runuser -u postgres -- createdb {}'.format(dbname), shell=True)
    subprocess.run('''sudo runuser -u postgres -- psql -c "CREATE USER {} with encrypted password '{}';"'''.format(username, password), shell=True)
    subprocess.run('''sudo runuser -u postgres -- psql -c "GRANT ALL PRIVILEGES ON DATABASE {} TO {}"'''.format(dbname, username), shell=True)

    # Restart Postgres
    subprocess.call(["sudo", "/etc/init.d/postgresql", "restart"])

    # Print success message
    print("PostgreSQL installed and configured successfully!")

# Install and configure virtualenv
def install_virtualenv():
    """
    This function is used to install virtualenv,
    a tool used to create isolated Python environments.
    It checks the status of the installation, creates a new virtualenv,
    and then activates it by running the pip install command with
    the contents of the requirements.txt file.
    """
    # Install virtualenv
    status = subprocess.call(["sudo", "apt-get", "install", "virtualenv"])
    if status != 0:
        print("Installation of virtualenv failed!")
    else:
        # Set up a new virtualenv
        subprocess.run("virtualenv env", shell=True)

        # Activate virtualenv
        subprocess.run("source env/bin/activate ; pip install -r requirements.txt ;", shell=True, executable='/bin/bash')

# Install supervisor
def install_supervisor():
    """
    This function installs the supervisor package on a system using
    the apt-get command.
    After installation, it checks if the installation was successful
    and prints an appropriate message.
    """
    os.system("sudo apt-get install supervisor -y")

    # Check if supervisor installation is successful
    if os.system("dpkg --get-selections | grep supervisor") != 0:
        print("Supervisor installation failed!")
    else:
        print("Supervisor installation successful!")

def reload_supervisor():
    """This function is used to reload the supervisor configuration.
    It runs the commands 'sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl start all',
    and if the command is successful, prints 'Successful reload of supervisor configuration',
    otherwise it prints 'Unsuccessful reload of supervisor configuration'."""

    # Reload supervisor configuration
    if os.system("sudo supervisorctl reread && sudo supervisorctl update && sudo supervisorctl start all") == 0:
        print('Successful reload of supervisor configuration')
    else:
        print('Unsuccessful reload of supervisor configuration')

def create_supervisor_config(program_name, command, conf_path):
    """
    This function creates a supervisor configuration file
    for a given program name, command, and configuration path.
    It writes the configuration details to the file and then copies
    it to the /etc/supervisor/conf.d/ directory. It also checks for
    any errors that might occur during the process.
    """
    exec_path = os.path.join(project_dir, command)

    # Create supervisor configuration file
    supervisor_conf_file = conf_path

    with open(supervisor_conf_file, 'w') as f:
        f.write(f'[program:{program_name}]\n')
        f.write(f'command={exec_path}\n')
        f.write(f'user={user_name}\n')
        f.write(f'directory={project_dir}\n')
        f.write(f'autostart=true\n')
        f.write(f'autorestart=true\n')
        f.write(f'startsecs=10\n')
        f.write(f'stopwaitsecs=600\n')

    # Copy the supervisor configuration file
    if os.system(f'sudo mv {supervisor_conf_file} /etc/supervisor/conf.d/') != 0:
        raise Exception('Failed to move supervisor config file.')


# Create a function to verify the inputs
def verify_input(prompt):
    while True:
        # Get the input from the user
        user_input = input(prompt)
        # Check if the input is a string with no spaces or uppercases
        if user_input.isalpha() and user_input.islower():
            # If it is, break out of the loop
            break
        else:
            # Else, show an error message and try again
            print("The input must be a string with no spaces or uppercases. Please try again.")
    return user_input


def is_host_or_ip(prompt):
    user_input = input(prompt)
    host_regex = r'^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$'
    ip_regex = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'
    while True:
        if re.match(host_regex, user_input) or re.match(ip_regex, user_input):
            return user_input
        else:
            user_input = input('Please enter a valid domain or IP address: ')

# Create a function to verify the passwords
def verify_password(prompt):
    while True:
        # Get the password from the user
        password = getpass.getpass(prompt)
        # Get a confirmation of the password
        password_confirm = getpass.getpass("Please confirm the password: ")
        # Check if the passwords match
        if password == password_confirm:
            # If they do, break out of the loop
            break
        else:
            # If they don't, show an error message and try again
            print("The passwords didn't match. Please try again.")
    return password


def generate_env(django_db_name, django_db_user, django_db_password, django_rabbitmq_host, django_rabbitmq_user, django_rabbitmq_password):
    env_file = open('.env', 'w')

    env_file.write("DJANGO_DB_NAME={}\n".format(django_db_name))
    env_file.write("DJANGO_DB_USER={}\n".format(django_db_user))
    env_file.write("DJANGO_DB_PASSWORD={}\n".format(django_db_password))
    env_file.write("DJANGO_RABBITMQ_HOST={}\n".format(django_rabbitmq_host))
    env_file.write("DJANGO_RABBITMQ_USER={}\n".format(django_rabbitmq_user))
    env_file.write("DJANGO_RABBITMQ_PASSWORD={}\n".format(django_rabbitmq_password))

    env_file.close()

def migrate():
    # Activate virtualenv
    subprocess.run("source env/bin/activate ; ./manage.py migrate ;", shell=True, executable='/bin/bash')
