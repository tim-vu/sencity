## Backend

#### Dependencies installeren
1. Installeer python virtual environments
> sudo apt-get install python3-venv
2. Maak een virtual environment aan
> python3 -m venv ~/.virtualenvs/sencity
3. Activeer de environment
> source ~/.virtualenvs/sencity/bin/activate
4. Navigeer naar de backend directory (bevat requirements.txt)
5. Installeer de dependencies
> pip install -r requirements.txt
6. Kies de juiste python interpreter in pycharm

### Migrations
1. Navigeer naar de backend directory
2. Maak de migrations aan (enkel nodig indien de models zijn veranderd)
> python manage.py makemigrations
3. Maak het schema aan op basis van de migrations
> python manage.py migrate

### De server runnen

Zorg er eerst voor dat je alle dependencies hebt geinstalleerd, je virtual environment is geactiveerd en de database is gemigrate.

> python manage.py runserver

### Admin account aanmaken (optioneel)

Met een admin account kan je inloggen op het admin paneel als je handmatig de gegevens in de database wilt aanpassen. Het admin paneel bevind zich op het pad /admin.

1. Navigeer naar de backend directory
2. Maak een admin account aan
> python manage.py createsuperuser
3. Volg de instructies









