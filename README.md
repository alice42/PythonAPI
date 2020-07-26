# ApiArcane

A RESTful API using [Flask](https://flask.palletsprojects.com/en/1.1.x/)

### Prerequisites

- [Python3](https://www.python.org/downloads/)
- [Pip3](https://pip.pypa.io/en/stable/installing/)
- [virtualenv](https://pypi.org/project/virtualenv/)

### Installation

Clone the git repository

```
$ git clone https://github.com/alice42/ApiArcane.git
$ cd ApiArcane
```

Create a virtualenv

```
$ virtualenv venv
```

and activate it

```
$ source venv/bin/activate
```

then install dependencies

```
$ pip3 install -r requirements.txt
```

Make sure to run the initial migration commands to update the database.

```
$ python3 manage.py db init
```

```
$ python3 manage.py db migrate --message 'initial database migration'
```

```
$ python3 manage.py db upgrade
```

Run the app

```
$ python3 manage.py run
```

### Viewing the app

    Open the following url on your browser to view swagger documentation
    http://127.0.0.1:5000/

### Using the app

    See [INSTRUCTIONS](https://github.com/alice42/ApiArcane/blob/master/INSTRUCTIONS.md) |
