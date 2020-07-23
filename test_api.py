import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import create_app
from models import setup_db, Actors, Movies

assistant_token = "Bearer {}".format(os.environ.get('ASSISTANT_TOKEN'))
director_token = "Bearer {}".format(os.environ.get('DIRECTOR_TOKEN'))
producer_token = "Bearer {}".format(os.environ.get('PRODUCER_TOKEN'))

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the CastingAgency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "castingagencytest"
        self.database_path = "postgresql://{}@{}/{}".format('postgres:0000', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_actor = {
            'name': 'Charlize Theron',
            'age': 44,
            'gender': 'Female'
        }

        self.new_movie = {
            'title': 'Interstellar',
            'release_date': '11-07-2014'
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_post_actor(self):
        res = self.client().post('/actors', json=self.new_actor, headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_post_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers={"Authorization": producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])

    def test_modify_actor(self):
        res = self.client().patch('/actors/1', json={'age': 40}, 
            headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updates'])

    def test_modify_movie(self):
        res = self.client().patch('/movies/2', json={'title': 'Fight Club'}, 
            headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['updates'])

    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers={"Authorization": director_token})
        data = json.loads(res.data)
        actor = Actors.query.filter(Actors.id == '2').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(actor, None)

    def test_delete_movie(self):
        res = self.client().delete('/movies/3', headers={"Authorization": producer_token})
        data = json.loads(res.data)
        movie = Movies.query.filter(Movies.id == '3').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(movie, None)

    def test_error_400(self):
        res = self.client().patch('/movies/1', json={'release_date': 30}, 
            headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_error_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_error_403(self):
        res = self.client().delete('/movies/3', headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    def test_error_404(self):
        res = self.client().patch('/actors/50', headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Page Not Found')

    def test_error_405(self):
            res = self.client().post('/actors/3', json=self.new_actor, headers={"Authorization": director_token})
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 405)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['message'], 'method not allowed')

    def test_error_422(self):
        res = self.client().delete('/movies/500', json={'release_date': 30}, 
            headers={"Authorization": producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()