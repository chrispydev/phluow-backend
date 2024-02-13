# How to start project

```bash
# create virtual environment
python -m venv venv

# on linux
source venv/bin/activate

# install modules
pip install -r requirements.txt

# create db
python manage.py makemigrations
python manage.py migrate

# to run server
python manage.py runserver
```
