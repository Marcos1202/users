#Para los archivos secretos
from django.core.exceptions import ImproperlyConfigured
import json

with open("secret.json") as f:
    secret=json.loads(f.read())

def get_secret(secret_name, secrets=secret):
    try:
        return secrets[secret_name]
    except:
        msg = "la variable %s no esiste" %secret_name
        raise ImproperlyConfigured(msg)
