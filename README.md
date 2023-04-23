# bookshelf-be
1. Create a virtual environment
```sh
py -m venv env
```

2. Activate the virtual env
```sh
.\env\Scripts\activate
```

3. Run migrations
```sh
py manage.py migrate
```

4. Create a superuser
```sh
py manage.py createsuperuser
```

5. Run the server
```sh
py manage.py runserver
```