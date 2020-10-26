# Blockchain Intent Management System (BIMS)

The Blockchain Intent Management System aims to simplify the process of 
blockchain selection by applying intent-based management. The system integrates 
the Intent Refinement Toolkit ([IRTK](https://gitlab.ifi.uzh.ch/scheid/irtk-code))
and connects to a policy-based blockchain selection framework called 
[PleBeuS](https://gitlab.ifi.uzh.ch/scheid/plebeus).

This system was developed as part of my Bachelor Thesis at University of Zurich.

## Code Structure

This structure is intended to find **important** files more easily. Thus, only important
files for the setup are mentioned.

```
bims
|___bims
|   |   settings.py
|
|___frontend
|
|___intent_manager
|
|___policy_manager
|
|___refiner
|   |___irtk
|   |   |   config.py
|
|___user_manager
|
|   manage.py

README.md
requirements.txt
currencies.json
logging.conf
package.json
```


## Setup

Note that for different operating systems the commands are slightly different.

#### Requirements
* Python 3.8 or later
* PostgreSQL
* Node.js and npm

#### Dependencies

1. Create and activate a virtual environment

```
$ python -m venv venv
```

activate on Unix
```
$ source venv/bin/activate
```

activate on Windows
```
C:\> venv\Scripts\activate.bat
```

2. Install the dependencies:

```
(venv) $ pip install -r requirements.txt
```

#### Database

1. Create a postgres database

    1.0 On Windows: start postgres server (path to PostgreSQL files might be different)
    ```
    C:\> pg_ctl -D "C:\Program Files\PostgreSQL\12\data" start
    ```

    1.1 Start PostgreSQL interactive terminal
    
    ```
    $ psql -U postgres
    ```
    
    1.2 Create a user
    ```
    # CREATE USER *username* WITH PASSWORD '*password*';  
    ```
    
    1.3 Create a database
    ```
    # CREATE DATABASE *database name* OWNER *username*;  
    ```
    
    1.4 Use `\q` to quit the PostgreSQL terminal

2. Update database settings in `settings.py`

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '*database name*',
        'USER': '*username*',
        'PASSWORD': '*password*',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

**Note that commands using `manage.py` should be run from the base directory, i.e. use `bims/manage.py`**

Make migrations

```
(venv) $ python bims/manage.py makemigrations
```

Migrate

```
(venv) $ python bims/manage.py migrate
```

Load currencies in database

```
(venv) $ python bims/manage.py loaddata currencies.json
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

in `bims/bims/settings.py`:

Use PleBeuS?
`USE_PLEBEUS=True` / `USE_PLEBEUS=False`

Configure PleBeuS server address and port: `PLEBEUS_URL=''`


#### Run server

1. Make sure database server is running

2. Run Django server:
```
(venv) $ python bims/manage.py runserver
```
By default, the server will run on 127.0.0.1:8000, however a different address and port
can be specified.


#### Run tests

```
(venv) $ python bims/manage.py test user_manager.tests
(venv) $ python bims/manage.py test intent_manager.tests
(venv) $ python bims/manage.py test policy_manager.tests.tests
(venv) $ python bims/manage.py test policy_manager.tests.plebeus_tests
(venv) $ python bims/manage.py test bims.integration_tests
```

## Troubleshooting

#### ```OperationalError: could not connect to server: Connection refused```

```
django.db.utils.OperationalError: could not connect to server: Connection refused (0x0000274D/10061)
could not connect to server: Connection refused (0x0000274D/10061)
	Is the server running on host "localhost" (127.0.0.1) and accepting
	TCP/IP connections on port 5432?
```

It seems like the database cannot be accessed. Make sure the PostgreSQL server is 
running at the specified address and port.


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
(venv) $ python -m nltk.downloader punkt
```
