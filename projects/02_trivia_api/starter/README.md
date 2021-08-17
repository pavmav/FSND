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

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable
- 405: Method not allowed

### Endpoints 
#### GET /categories
- General:
    - Returns a list of categories names as a list 
- Sample: `curl localhost:5000/categories`

``` 
{
  "books": [
    {
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ]
}
```
#### GET /questions?page=page_number
- General:
    - Returns a list of questions objects, categories, current category (default=null) and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl localhost:5000/questions?page=2`

``` 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "Escher", 
      "category": 2, 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": 2, 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": 2, 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": 2, 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": 4, 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }, 
    {
      "answer": "Me", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "Who?"
    }, 
    {
      "answer": "Because I can", 
      "category": 2, 
      "difficulty": 4, 
      "id": 28, 
      "question": "Why?"
    }
  ], 
  "total_questions": 21
}  
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. 
- Sample: `curl -X DELETE localhost:5000/questions/29`
```
{
  "success": true
}
```

#### POST /questions (Create question variant)
- General:
    - Creates a new question using the submitted question text, answer, difficulty and category. Returns the id of the created question and success value. 
- Sample: `curl -X POST localhost:5000/questions -H "Content-Type: application/json" --data '{"question": "Foo?", "answer":"Bar!", "difficulty":"5", "category":"1"}'`
  
```
{
  "question_id": 30, 
  "success": true
}
```

#### POST /questions (Search question variant)
- General:
    - Searches questions by search term in question texts and returns a list of questions objects, categories, current category (default=null) and total number of questions.
- Sample: `curl -X POST localhost:5000/questions -H "Content-Type: application/json" --data '{"searchTerm":"who"}'`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Me", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "Who?"
    }
  ], 
  "total_questions": 3
}
```

#### GET /categories/{category_id}/questions
- General:
    - Returns a list of questions objects in a category with id=category_id, categories, current category and total number of questions
- Sample: `curl localhost:5000/categories/1/questions`

``` 
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": null, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Me", 
      "category": 1, 
      "difficulty": 1, 
      "id": 24, 
      "question": "Who?"
    }, 
    {
      "answer": "Bar!", 
      "category": 1, 
      "difficulty": 5, 
      "id": 30, 
      "question": "Foo?"
    }
  ], 
  "total_questions": 5
} 
```

#### POST /quizzes
- General:
    - Returns question object based on submitted information: category and IDs of the questions, that already were asked. 
- Sample: `curl -X POST localhost:5000/quizzes -H "Content-Type: application/json" --data '{"previous_questions":[20], "quiz_category": {"type":"Science", "id":"0"}}'`
  
```
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }
}
```

## Deployment N/A

## Authors
Udacity team and Pavel Mavrichev

## Acknowledgements 
Udacity team and Coach Caryn!