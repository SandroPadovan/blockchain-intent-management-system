# Blockchain Intent Management System (BIMS)

The Blockchain Intent Management System aims to simplify the process of 
blockchain selection by applying intent-based management. The system integrates 
the Intent Refinement Toolkit ([IRTK](https://gitlab.ifi.uzh.ch/scheid/irtk-code))
and connects to a policy-based blockchain selection framework called 
[PleBeuS](https://gitlab.ifi.uzh.ch/scheid/plebeus).

This system was developed as part of my Bachelor Thesis at University of Zurich.


## Setup

Note that for different operating systems the commands are slightly different.

#### Requirements
* Python 3
* virtualenv
* PostgreSQL
* Node.js and npm

#### Dependencies

1. Create a virtual environment

2. Install the dependencies:

```
(venv) $ pip install -r requirements.txt
```

#### Database

1. Create a postgres database

2. Update database settings in `settings.py`

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '*Name of DB*',
        'USER': '*Name of User*',
        'PASSWORD': '*Password*',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. Make migrations

```
$ python bims\manage.py makemigrations
```

4. Migrate

```
$ python bims\manage.py migrate
```

Load currencies in database

```
$ python bims\manage.py loaddata currencies.json
```

#### GUI

Install dependencies
```
$ npm install
```

Build project
```
$ npm run build
```

#### Configure PleBeuS

in `bims\settings.py`:

Use PleBeuS?
`USE_PLEBEUS=True` / `USE_PLEBEUS=False`

Configure PleBeuS server URL: `PLEBEUS_URL=''`


#### Run server

1. Make sure database server is running

2. Run Django server:
```
$ python bims\manage.py runserver
```

#### Run tests

```
$ python bims\manage.py test user_manager.tests
$ python bims\manage.py test intent_manager.tests
$ python bims\manage.py test policy_manager.tests.tests
$ python bims\manage.py test policy_manager.tests.plebeus_tests
$ python bims\manage.py test bims.integration_tests
```

## Troubleshooting

#### ```KeyError: 'formatters'```

This is an issue with the IRTK logger.

Run your command from the same directory as the `logging.conf` file. 


#### ```LookupError: Resource punkt not found```

```
LookupError: Resource punkt not found.
Please use the NLTK Downloader to obtain the resource:

>>> import nltk
>>> nltk.download('punkt')

Attempted to load tokenizers/punkt/PY3/english.pickle
```

This error message indicates that the punkt resource from the nltk data is missing.
It is required for tokenizing the intents.
To resolve the issue run:

```console
$ python -m nltk.downloader punkt
```
