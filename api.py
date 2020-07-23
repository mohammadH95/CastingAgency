import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from flask_cors import CORS
from models import setup_db, Movies, Actors
from auth.auth import AuthError, requires_auth

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # GET all Actors 
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(token):
        actors = Actors.query.all()        
        actors_formatted = [actor.format() for actor in actors]

        return jsonify({
            'success': True,
            'actors': actors_formatted
        })


    # GET all Movies
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(token):
        movies = Movies.query.all()
        movies_formatted = [movie.format() for movie in movies]

        return jsonify({
            'success': True,
            'movies': movies_formatted
        })


    # POST new actors
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(token):
        try:
            body = request.get_json()

            new_name = body.get('name', None)
            new_age = body.get('age', None)
            new_gender = body.get('gender', None)

            actor = Actors(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            actor = actor.format()
            
            return jsonify({
                'success': True,
                'created': actor
            })    
        except:
            abort(422)
        

    # POST new movies
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(token):
        try:
            body = request.get_json()

            new_title = body.get('title', None)
            new_date = body.get('release_date', None)

            movie = Movies(title=new_title, release_date=new_date)
            movie.insert()
            movie = movie.format()

            return jsonify({
                'success': True,
                'created': movie,
            })    
        except:
            abort(422)
        

    # Modify actor
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def modify_actor(token, actor_id):
        actor = Actors.query.get(actor_id)
        if not actor:
            abort(404)

        body = request.get_json()

        new_name = body.get('name', actor.name)
        new_age = body.get('age', actor.age)
        new_gender = body.get('gender', actor.gender)

        actor.name = new_name
        actor.age = new_age
        actor.gender = new_gender

        actor.update()
        actor = actor.format()

        return jsonify({
            'success': True,
            'updates': actor
        }) 



    # Modify movie
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def modify_movie(token, movie_id):
        try:
            movie = Movies.query.get(movie_id)
            if movie is None:
                abort(404)

            body = request.get_json()

            new_title = body.get('title', movie.title)
            new_date = body.get('release_date', movie.release_date)

            movie.title = new_title
            movie.release_date = new_date

            movie.update()
            movie = movie.format()

            return jsonify({
                'success': True,
                'updates': movie
            })    
        except:
            abort(400)
        

    # DELETE actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(token, actor_id):
        try:
            actor = Actors.query.get(actor_id)
            if actor is None:
                abort(404)

            actorD = actor.format()
            actor.delete()

            return jsonify({
                'success': True,
                'deleted': actorD
            })    
        except:
            abort(422)
        

    # DELETE movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_user(token, movie_id):
        try:
            movie = Movies.query.get(movie_id)
            if movie is None:
                abort(404)

            movieD = movie.format()
            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movieD
            })    
        except:
            abort(422)
        

    # Errors handlers
    @app.errorhandler(AuthError)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error["description"]
        }), error.status_code

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "Page Not Found"
            }), 404
        
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
            }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request"
            }), 400

    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
            }), 405

    return app

    

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)