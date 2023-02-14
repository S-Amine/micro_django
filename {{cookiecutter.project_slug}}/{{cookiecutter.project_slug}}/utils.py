# A function to get the sensitive settings from .env file

def get_django_settings(env_file):
    data = {}
    with open(env_file) as f:
        for line in f:
            key_value = line.split('=')
            if len(key_value) == 2:
                key, value = key_value
                if key.startswith('DJANGO_'):
                    data[key] = value.strip() # strip whitespace
    return data

# Colors for print use

colors = {
    "yellow": "\033[1;33m",
    "green": "\033[1;32m",
    "cyan": "\033[1;36m",
    "red": "\033[1;31m",
    "white": "\033[1;37m"
}
