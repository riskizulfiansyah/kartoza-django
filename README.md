# kartoza-django

## Requirement:

- postgresql
- postgis
- libgeos-dev
- libgdal-dev

## Getting Started
1. install with ubuntu
   ```
   sudo apt-get install postgis libgeos-dev libgdal-dev
   ```
2. install package
   ```
   sudo pip install -r requirements.txt
   ```
3. create db
   ```
   sudo -u postgres createdb -T template_postgis kartoza_django
   ```
4. Create .env file and assign env value
    ```
    cp .env.example .env
    ```
4. run migration
   ```
   python manage.py migrate
   ```
5. create super user
   ```
   python manage.py createsuperuser
   ```

## How to Run
```
python manage.py runserver
```

## How to unit test
1. Run unit test
    ```
    coverage run --source='.' manage.py test
    ```
2. Show report
    ```
    coverage report -m
    ```