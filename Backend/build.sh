#!/usr/bin/env bash

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

python manage.py shell -c "
import os
from django.contrib.auth.models import User

username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'barkaalice00@gmail.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'Alicebrk12')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print('Superuser créé')
else:
    print('Superuser existe déjà')
"