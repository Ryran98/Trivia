# Udacity Trivia App

## Introduction
This project serves as a display of all the elements learned as part of the 2nd Module (API Development and Documentation) that makes up the Full Stack Web Developer Nanodegree Program.

The aim is to build an effective RESTful API in Python using the Flask framework which serves a Trivia FrontEnd Web Application built in React.js.

## Setup Instructions

### Backend
To start you will need to install the dependencies for the backend. You can do this using pip by navigating to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```

You will then need to set up the Database with the following command:
```bash
psql trivia < trivia.psql
```

And then to run the backend server, you will need to execute:
```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export FLASK_DEBUG=1
python -m flask run
```

To run the tests, run from the `/backend` directory:
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

### Front end
To start, you will need to install Node and Node Package Manager (NPM) in order to to install the project dependencies for the front end.

You can download and install Node and NPM [here](https://nodejs.org/en/download/)

Once you have them both installed, navigate to the `/frontend` directory and run:
```bash
npm install
```

Once you've installed all of the project dependencies you can finally run the following to start the front end server
```bash
npm start
```

## API Endpoints

### Base URL
This app can currently only be run locally and is not hosted as a base URL. Therefore the backend server is hosted at the default http://127.0.0.1:5000/.

### Authentication
This version of the application does not require any type of authentication or API keys.

### Error Handling
Any errors that occur in the backend are return as JSON objects in the following format:
```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return the following error types:
- 404: Resource Not Found
- 422: Not Processable
- 400: Bad Request
- 405: Method Not Allowed

### Endpoints

#### GET /categories
- Returns a list of all categories
- Example: `curl http://127.0.0.1:5000/categories`
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
  "success": true
}
```

#### GET /questions
- Returns a list of questions, the total number of questions, and a list of all categories
- Questions are paginated in groups of 10. You can specify the page number as a request parameter in the URL
- Example: `curl http://127.0.0.1:5000/questions?page=1`
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
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

#### DELETE /questions/{question_id}
- Deletes the question for the given question ID if it exists
- Returns the ID of the question that has been deleted
- Example: `curl -X DELETE http://127.0.0.1:5000/questions/2`
```
{
  "id": 2,
  "success": true
}
```

#### POST /questions
- Creates a new question using the question text, answer text, difficulty and category passed in to the request body as JSON. Returns the ID of the new question
- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Is this the best test question ever?", "answer":"yes", "difficulty":"1", "category":"5"}'`
```
{
    "id": 26,
    "success": true
}
```
- This endpoint can also be used to return a list of questions based on a search term which is also passed in to the request body as JSON. Returns any questions for whom the search term is a substring of the question
- Example: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"title"}'`
```
{
    "current_category": null,
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```

#### GET /categories/{category_id}/questions
- Returns all questions for the given category ID, paginated 10 at a time as well as the total number of questions and current category. As with the /questions GET endpoint, the page number can be specified as a request parameter in the URL
- Example: `curl http://127.0.0.1:5000/categories/5/questions`
```
{
  "current_category": "Entertainment",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "This one",
      "category": 5,
      "difficulty": 4,
      "id": 24,
      "question": "What is the best test question ever?"
    },
    {
      "answer": "yes",
      "category": 5,
      "difficulty": 1,
      "id": 26,
      "question": "Is this the best test question ever?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

#### POST /quizzes
- This endpoint is used to play the Trivia Quiz. It takes a category and previous questions from the request body as JSON.
- Returns a random question for the given category which isn't one of the previous questions
- Example: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"id":5}, "previous_questions":[]}'`
```
{
    "question": {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    "success": true
}
```