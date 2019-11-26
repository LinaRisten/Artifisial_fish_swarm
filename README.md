# Artifisial_fish_swarm

## About
Some kind of calculator

## Install

Install requirements:

```
pip install -r  requirements.txt 
```

Create general migrations:

```
python3 manage.py makemigrations
```

Create migrations for afs:

```
python manage.py makemigrations afs
```

Migrate:

```
python manage.py migrate
```

Create superuser:

```
python manage.py createsuperuser
```

For run server execute: 

```
python manage.py runserver <host>:<port>
```

Example run server:

```
python manage.py runserver 0.0.0.0:8000
```

## Useful

Create virtual enironment:

```
python3 -m venv <name_venv>
```

Activate virtual environment:

```
source <name_venv>/bin/activate
```

Deactivate virtual environment:

```
deactivate
```
