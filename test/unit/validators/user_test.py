import pytest

import validators


class TestUserPostScheme():

    @classmethod
    def setup_class(cls):
        cls.validator = validators.UserPostSchema()

    def test_validate_successfully(self):
        posted_data = {
            'name': 'Steve Jobs',
            'age': 30,
            'gender': 'male',
            'email': 'steve@jobs.com'
        }
        errors = self.validator.validate(posted_data)
        assert errors == {}

    def test_validate_with_gender(self):
        posted_data = {
            'name': 'Steve Jobs',
            'age': 30,
            'gender': 'superman',
            'email': 'steve@jobs.com'
        }
        errors = self.validator.validate(posted_data)
        assert errors == {'gender': ["Gender must be 'male' or 'female'"]}


class TestUserPutSchema(object):

    @classmethod
    def setup_class(cls):
        cls.validator = validators.UserPutSchema()

    def test_validate_successfully(self):
        put_data = {
            'name': 'Steve Jobs',
            'age': 30,
            'gender': 'male',
            'email': 'steve@jobs.com'
        }
        errors = self.validator.validate(put_data)
        assert errors == {}

    def test_validate_with_gender(self):
        put_data = {
            'name': 'Steve Jobs',
            'age': 30,
            'gender': 'superman',
            'email': 'steve@jobs.com'
        }
        errors = self.validator.validate(put_data)
        assert errors == {'gender': ["Gender must be 'male' or 'female'"]}
