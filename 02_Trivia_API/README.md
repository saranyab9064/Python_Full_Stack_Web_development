# Full Stack API Final Project

## Full Stack Trivia
Trivia API is a web application , allows peope to hold trivia on a regular basis  and play the game, 
but their API experience is limited and still needs to be built out. 

The following are the pending steps which has been implemented:

1) Display questions - both all questions and by category. Questions should show the question, 
category and difficulty rating by default and can show/hide the answer. 
2) Delete questions.
3) Add questions and require that they include question and answer text.
4) Search for questions based on a text query string.
5) Play the quiz game, randomizing either all questions or within a specific category. 

## Getting Started
## Installing Dependencies
### Python 3.7
Install the latest version of python on local machine
(https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)
#### PIP Dependencies
Navigate to the '/backend' directory and run the text file. The text file will install all
necessary packages for running our project file on local machine

```bash
pip3 install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```
## Running the server

From within the `backend` directory

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```

#### Frontend Dependencies

This project uses NPM to manage software dependencies. from the `frontend` directory run:

```bash
npm install
```

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## API Reference

### Getting Started

* Backend Base URL: `http://127.0.0.1:5000/`
* Frontend Base URL: `http://127.0.0.1:3000/`


### Error Handling

Errors are returned in the following json format:

```json
      {
        "success": "True or False",
        "error": "Error code ",
        "message": "Error Message",
      }
```

The error codes are:


* 404 – Page Not Found/Resource not found
* 422 – Unprocessable entity
* 500 – Internal Server error

### Endpoints
The following are the endpoints:
* GET '/questions'
* POST '/questions'
* DELETE '/questions
* GET '/categories'
* GET '/categories/<int:category_id>/questions'
* POST '/search'
* GET '/quizzes'
#### GET /categories

- General: 
  - Returns all the categories.

- Testing Command:  `curl http://127.0.0.1:5000/categories`
```json
    {
    "categories": {
        "1": "Science", 
        "2": "Art", 
        "3": "Geography", 
        "4": "History", 
        "5": "Entertainment", 
        "6": "Sports"
    }, 
    "status": 200, 
    "success": true
    }

```
#### GET /questions
- General:
  - Returns all questions
  - questions are in a paginated.
  - pages could be requested by a query string

- Testing Command: `curl http://127.0.0.1:5000/questions`<br>
```json
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
#### DELETE /questions/<int:id>


- General:
  - Deletes a question by id form the url parameter.

- Testing Command: `curl http://127.0.0.1:5000/questions/6 -X DELETE`
```json
{
  "message": "Question successfully deleted", 
  "status": 200, 
  "success": true
}

```
#### POST /questions

- General:
  - Creates a new question based on a payload.
  - Testing Command: `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{
            'question': 'What is the most beautiful park in the world?',
            'answer': 'Hyde Park, London',
            'category': 3,
            'difficulty': 1
        }'`
 ```json       
{
  "message": "Question successfully created!",
  "status": 200, 
  "success": true
}
```
#### POST /questions/search

- General:
  - returns questions that has the search substring

- Testing Command: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Taj Mahal"}'`
```json
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true
}
```
#### GET /categories/<int:category_id>/questions

- General:
  - Gets questions by category using the id from the url parameter.
- Testing Command: `curl http://127.0.0.1:5000/categories/1/questions`<br>

```json
{
  "current_category": 1, 
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
      "answer": "cbe", 
      "category": 1, 
      "difficulty": 1, 
      "id": 25, 
      "question": "what is your city"
    }
  ], 
  "success": true, 
  "total_questions": 4
}
```
#### POST /quizzes

- General
  - Takes the category and previous questions in the request.
  - Return random question not in previous questions.

- Testing Command: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [5, 9],
                                            "quiz_category": {"type": "History", "id": "4"}}'`
```json
{
  "question": {
    "answer": "George Washington Carver",
    "category": 4,
    "difficulty": 2,
    "id": 12,
    "question": "Who invented Peanut Butter?"
  },
  "success": true
}

```
## Authors
- Saranya Balakrishnan worked on the API and test suite to integrate with the frontend
- Udacity provided the starter code for this project.
