# Full Stack Casting Agency

## Getting Started

### Installing Dependencies

#### Python

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the wouldyourather.psql file provided. From the backend folder in terminal run:
```bash
psql castingagency < castingagency.psql
```

## Running the server
From within the `backend` directory first ensure you are working using your created virtual environment.
To run the server, execute:
```bash
python api.py OR python3 api.py
```

## Authorization
The API uses the Auth0 Role Based Access Control mechanisms for implementing authorization for endpoints. The Roles and their permissions are:
* Assistant: [
    get:actors,
    get:movies
]
* Director: [
    ..all assistant permissions,
    post:actors,
    delete:actors,
    patch:actors,
    patch:movies
]
* Producer: [
    ..all director permissions,
    post:movies,
    delete:movies
]

## API Reference

### Getting Started
- Base URL: https://castingagencyfs.herokuapp.com/

### Endpoints

#### GET /actors
- Get actors data
- Request Arguments: None
- Response:
```
{
  "actors": [
    {
      "age": 42,
      "gender": "Male",
      "id": 1,
      "name": "Tom Hardy"
    },
    {
      "age": 32,
      "gender": "Female",
      "id": 2,
      "name": "Ana de Armas"
    }
  ],
  "success": true
}
```

#### GET /movies
- Get movies data
- Request Arguments: None
- Response:
```
{
  "movies": [
    {
      "id": 2,
      "release_date": "Fri, 04 Oct 2019 00:00:00 GMT",
      "title": "Joker"
    },
    {
      "id": 3,
      "release_date": "Fri, 26 Apr 2019 00:00:00 GMT",
      "title": "Avengers: Endgame"
    }
  ],
  "success": true
}
```

#### POST /actors
- Create new actor
- Request Arguments: None
- Request body:{name:string, age:intger, gender:string}
- Response:
```
{
  "created": {
    "age": 44,
    "gender": "Female",
    "id": 8,
    "name": "Charlize Theron"
  },
  "success": true
}
```

#### POST /movies
- Create new movies
- Request Arguments: None
- Request body:{title:string, release_date:date}
- Response:
```
{
  "created": {
    "id": 8,
    "release_date": "Fri, 07 Nov 2014 00:00:00 GMT",
    "title": "Interstellar"
  },
  "success": true
}
```

#### PATCH /actors/{actor_id}
- Modify the actor
- Request Arguments: actor_id
- Request body:{name:string, age:intger, gender:string}
- Response:

```
{
  "success": true,
  "updates": {
    "age": 40,
    "gender": "Male",
    "id": 1,
    "name": "Tom Hardy"
  }
}
```

#### PATCH /movies/{movie_id}
- Modify the movie
- Request Arguments: movie_id
- Request body:{title:string, release_date:date}
- Response:

```
{
  "success": true,
  "updates": {
    "id": 2,
    "release_date": "Tue, 10 Sep 2019 00:00:00 GMT",
    "title": "Joker"
  }
}
```

#### DELETE /actors/{actor_id}
- Delete actor
- Request Arguments: actor_id
- Response:
```
{
  "deleted": {
    "age": 40,
    "gender": "Male",
    "id": 1,
    "name": "Tom Hardy"
  },
  "success": true
}
```

#### DELETE /movies/{movie_id}
- Delete movie
- Request Arguments: movie_id
- Response:
```
{
  "deleted": {
    "id": 2,
    "release_date": "Tue, 10 Sep 2019 00:00:00 GMT",
    "title": "Joker"
  },
  "success": true
}
```

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "Page Not Found"
}
```
The API will return error types when requests fail:
- 401: Unauthorized
- 403: Forbidden 
- 404: Resource Not Found
- 405: Method not allowed
- 422: Not Processable

## Testing
To run the tests, run
```
dropdb castingagencytest
createdb castingagencytest
psql castingagencytest < castingagency.psql
python test_api.py
```