import os

from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS

from utils import response
import validators
import config

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config.from_object(config.object_name[app.config['ENV']])
PORT = os.getenv('PORT', default=app.config['PORT'])
MONGODB_URI = os.getenv('MONGODB_URI', default=app.config['MONGODB_URI'])
MONGODB_DATABASE_NAME = os.getenv(
    'MONGODB_DATABASE_NAME', default=app.config['MONGODB_DATABASE_NAME'])

client = MongoClient(MONGODB_URI)
db = client[MONGODB_DATABASE_NAME]

users = db['users']


def user_exists(email):
    if users.count_documents({'email': email}) == 0:
        return False
    return True


def convert_user_object_from(user_doc):
    user = {}
    user['_id'] = str(user_doc['_id'])
    user['name'] = user_doc['name']
    if 'age' in user_doc:
        user['age'] = user_doc['age']
    if 'gender' in user_doc:
        user['gender'] = user_doc['gender']
    user['email'] = user_doc['email']
    return user


class Users(Resource):
    def post(self):
        poseted_data = request.get_json()

        errors = validators.UserPostSchema().validate(poseted_data)
        if bool(errors):
            error_data = {
                'errors': errors
            }
            return response.failure(error_data, 400)

        new_user = {}
        new_user['name'] = poseted_data['name']
        if 'age' in poseted_data:
            new_user['age'] = poseted_data['age']
        if 'gender' in poseted_data:
            new_user['gender'] = poseted_data['gender']
        new_user['email'] = poseted_data['email']

        if user_exists(new_user['email']):
            error_data = {
                'errors': {
                    'message': 'The user already exists'
                }
            }
            return response.failure(error_data, 400)

        result = users.insert_one(new_user)
        new_user['_id'] = str(result.inserted_id)

        return response.success(new_user)

    def get(self, user_id=None):
        # One
        if user_id is not None:
            user_doc = users.find_one({'_id': ObjectId(user_id)})
            user = convert_user_object_from(user_doc)
            return response.success(user)

        # Many
        cursor = users.find({})
        existing_users = []
        for user_doc in cursor:
            user = convert_user_object_from(user_doc)
            existing_users.append(user)
        return response.success(existing_users)

    def delete(self, user_id=None):
        if user_id is None:
            error_data = {
                'errors': {
                    'message': "The parameter 'user_id' is required"
                }
            }
            return response.failure(error_data, 400)

        result = users.delete_one({'_id': ObjectId(user_id)})
        if result.deleted_count == 0:
            error_data = {
                'errors': {
                    'message': "The user doesn't exist"
                }
            }
            return response.failure(error_data, 404)
        else:
            return response.success({
                '_id': user_id
            })

    def put(self, user_id=None):
        if user_id is None:
            error_data = {
                'errors': {
                    'message': "The parameter 'user_id' is required"
                }
            }
            return response.failure(error_data, 400)

        poseted_data = request.get_json()

        errors = validators.UserPutSchema().validate(poseted_data)
        if bool(errors):
            error_data = {
                'errors': errors
            }
            return response.failure(error_data, 400)

        update_user = {}
        if 'name' in poseted_data:
            update_user['name'] = poseted_data['name']
        if 'age' in poseted_data:
            update_user['age'] = poseted_data['age']
        if 'gender' in poseted_data:
            update_user['gender'] = poseted_data['gender']
        if 'email' in poseted_data:
            update_user['email'] = poseted_data['email']

        if not bool(update_user):
            error_data = {
                'errors': {
                    'message': "Nothing to update"
                }
            }
            return response.failure(error_data, 400)

        result = users.update_one({
            '_id': ObjectId(user_id)
        }, {
            '$set': update_user
        })
        if result.modified_count == 0:
            error_data = {
                'errors': {
                    'message': "The user doesn't exist"
                }
            }
            return response.failure(error_data, 404)
        else:
            return response.success({
                '_id': user_id
            })


api.add_resource(Users,
                 '/api/users',
                 '/api/users/<user_id>'
                 )

if app.config['REMOTE_DEBUGGING']:
    import ptvsd
    ptvsd.enable_attach(
        address=('0.0.0.0', app.config['REMOTE_DEBUGGING_PORT']), redirect_output=True)
    ptvsd.wait_for_attach()
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)
