import json

from bson.objectid import ObjectId

from app import app, users


class TestApp():

    @classmethod
    def setup_class(cls):
        cls.client = app.test_client()
        cls.users_col = users

    @classmethod
    def teardown_class(cls):
        cls.users_col.delete_many({})

    def setup_method(self):
        self.users_col.delete_many({})

    def test_get_users(self):
        self.users_col.insert_many([
            {
                '_id': ObjectId('5bda2c699f4db500ca1606fe'),
                'name': 'Steve Jobs',
                'age': 30,
                'gender': "male",
                'email': "steve@jobs.com"
            },
            {
                '_id': ObjectId('5bda2cd89f4db500e03c5014'),
                'name': 'Audrey Hepburn',
                'age': 22,
                'gender': 'female',
                'email': "audrey@hepburn.com"
            }
        ])

        result = self.client.get('/api/users')
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 200
        assert data_dict == {
            'status': 'success',
            'data': [
                {
                    '_id': '5bda2c699f4db500ca1606fe',
                    'name': 'Steve Jobs',
                    'age': 30,
                    'gender': "male",
                    'email': "steve@jobs.com"
                },
                {
                    '_id': '5bda2cd89f4db500e03c5014',
                    'name': 'Audrey Hepburn',
                    'age': 22,
                    'gender': 'female',
                    'email': "audrey@hepburn.com"
                }
            ]
        }

    def test_get_empty_users(self):
        result = self.client.get('/api/users')
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 200
        assert data_dict == {'status': 'success', 'data': []}

    def test_get_a_user(self):
        user_id = '5bda2c699f4db500ca1606fe'
        self.users_col.insert_one(
            {
                '_id': ObjectId(user_id),
                'name': 'Steve Jobs',
                'age': 30,
                'gender': "male",
                'email': "steve@jobs.com"
            }
        )

        result = self.client.get('/api/users/' + user_id)
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 200
        assert data_dict == {
            'status': 'success',
            'data': {
                '_id': '5bda2c699f4db500ca1606fe',
                'name': 'Steve Jobs',
                'age': 30,
                'gender': 'male',
                'email': 'steve@jobs.com'
            }
        }

    def test_post_a_user(self):
        data = {
            'name': 'Steve Jobs',
            'age': 30,
            'gender': "male",
            'email': "steve@jobs.com"
        }
        result = self.client.post('/api/users', json=data)
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 200
        assert data_dict['status'] == 'success'
        assert data_dict['data']['name'] == data['name']
        assert data_dict['data']['age'] == data['age']
        assert data_dict['data']['gender'] == data['gender']
        assert data_dict['data']['email'] == data['email']

    def test_post_a_user_with_missing_name_parameters(self):
        data = {
            'age': 30,
            'gender': "male",
            'email': "steve@jobs.com"
        }
        result = self.client.post('/api/users', json=data)
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 400
        assert data_dict == {'status': 'failure', 'data': {
            'errors': {'name': ['Missing data for required field.']}}}

    def test_post_a_user_when_alrady_a_user_exists(self):
        email = 'steve@jobs.com'
        self.users_col.insert_one(
            {
                '_id': ObjectId('5bda2c699f4db500ca1606fe'),
                'name': 'Steve Jobs',
                'age': 30,
                'gender': 'male',
                'email': email
            }
        )

        data = {
            'name': 'Tom Brown',
            'age': 45,
            'gender': 'male',
            'email': email
        }
        result = self.client.post('/api/users', json=data)
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 400
        assert data_dict == {'status': 'failure', 'data': {
            'errors': {'message': 'The user already exists'}}}

    def test_put_a_user(self):
        user_id = '5bda2c699f4db500ca1606fe'
        self.users_col.insert_one(
            {
                '_id': ObjectId(user_id),
                'name': 'Steve Jobs',
                'age': 30,
                'gender': 'male',
                'email': 'steve@jobs.com'
            }
        )

        update_data = {
            'name': 'Taylor Swift',
            'age': 28,
            'gender': 'female',
            'email': 'taylor@swift.com'
        }
        result = self.client.put('/api/users/' + user_id, json=update_data)
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 200
        assert data_dict['status'] == 'success'
        assert data_dict['data']['_id'] == user_id

        db_data = self.users_col.find_one({'_id': ObjectId(user_id)})
        assert db_data['name'] == update_data['name']
        assert db_data['age'] == update_data['age']
        assert db_data['gender'] == update_data['gender']
        assert db_data['email'] == update_data['email']

    def test_put_a_user_with_worng_gender_parameters(self):
        user_id = '5bda2c699f4db500ca1606fe'
        self.users_col.insert_one(
            {
                '_id': ObjectId(user_id),
                'name': 'Steve Jobs',
                'age': 30,
                'gender': 'male',
                'email': 'steve@jobs.com'
            }
        )

        update_data = {
            'name': "IKKOU",
            'age': 50,
            'gender': "okama",
            'email': "ikkou@san.com"
        }
        result = self.client.put('/api/users/' + user_id, json=update_data)
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 400
        assert data_dict == {'status': 'failure', 'data': {
            'errors': {'gender': ["Gender must be 'male' or 'female'"]}}}

    def test_put_a_user_without_user_id(self):
        result = self.client.put('/api/users', json={})
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 400
        assert data_dict == {'status': 'failure', 'data': {
            'errors': {'message': "The parameter 'user_id' is required"}}}

    def test_put_a_user_with_empty_data(self):
        result = self.client.put(
            '/api/users/5bda2c699f4db500ca1606fe', json={})
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 400
        assert data_dict == {'status': 'failure', 'data': {
            'errors': {'message': 'Nothing to update'}}}

    def test_put_a_user_when_the_user_does_not_exist(self):
        result = self.client.put(
            '/api/users/5bda2c699f4db500ca1606fe', json={
                'name': 'Taylor Swift',
                'age': 28,
                'gender': 'female',
                'email': 'taylor@swift.com'
            })
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 404
        assert data_dict == {'status': 'failure', 'data': {
            'errors': {'message': "The user doesn't exist"}}}

    def test_delete_a_user(self):
        user_id = '5bda2c699f4db500ca1606fe'
        self.users_col.insert_one(
            {
                '_id': ObjectId(user_id),
                'name': 'Steve Jobs',
                'age': 30,
                'gender': "male",
                'email': "steve@jobs.com"
            }
        )

        result = self.client.delete('/api/users/' + user_id)
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 200
        assert data_dict['status'] == 'success'
        assert data_dict['data']['_id'] == user_id

        db_data = self.users_col.find_one({'_id': ObjectId(user_id)})
        assert db_data is None

    def test_delete_a_user_without_user_id(self):
        result = self.client.delete('/api/users', json={})
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 400
        assert data_dict == {'status': 'failure', 'data': {
            'errors': {'message': "The parameter 'user_id' is required"}}}

    def test_delete_a_user_when_the_user_does_not_exist(self):
        result = self.client.delete('/api/users/5bda2c699f4db500ca1606fe')
        status_code = result.status_code
        data_dict = json.loads(result.data.decode('utf8'))

        assert status_code == 404
        assert data_dict == {'status': 'failure', 'data': {
            'errors': {'message': "The user doesn't exist"}}}
