# Udacitrivia

This project is a quiz engine. Users can create and browse questions divided into categories and play trivia using those questions. 

As a part of the Fullstack Nanodegree, it serves as a practice module for lessons from Course 2: API Development and Documentation.  

All backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines. Also the project was cteated to work with Postgresql db server, though it should be possible to use other databases with some changes.

#### Database

To populate the database with categories and starter questions you can use SQL script in /backend/trivia.psql file. To use it run the following command from /backend directory:
```
psql YOUR_DB_NAME -U YOUR_DB_USER < trivia.psql
```
You will need main database and one more database for tests. The default names are 'trivia' and 'trivia_test'.

You can set DB options through environment variables:
- DB_HOST default: localhost:5432
- DB_USER default: postgres
- DB_PASSWORD default: postgres
- DB_NAME = default: trivia (or trivia_test for tests)

To set an environment variable run the following command:
```
export VARIABLE=VALUE
```

#### Backend

From the /backend folder run `pip install requirements.txt`. All required packages are included in the requirements file.

The project mostly uses various Flask libraries and SQLAlchemy to interact with database.

To run the application run the following commands from /backend folder: 
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. If running locally on Windows, look for the commands in the [Flask documentation](http://flask.pocoo.org/docs/1.0/tutorial/factory/).

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000.

### Tests
In order to run tests navigate to the backend folder and run the following commands: 

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

The first time you run the tests, omit the dropdb command. 

All tests are kept in that file and should be maintained as updates are made to app functionality.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys.