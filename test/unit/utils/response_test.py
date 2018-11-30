from utils import response


class TestResponse():

    def test_return_success(self):
        data = {
            'name': 'Steve Jobs',
            'age': 30,
            'gender': "male",
            'email': "steve@jobs.com"
        }
        r, status_code = response.success(data)
        assert r == {
            'status': 'success',
            'data': data
        }
        assert status_code == 200

    def test_return_failure(self):
        data = {
            'errors': {
                'message': 'ERROR'
            }
        }
        r, status_code = response.failure(data, 400)
        assert r == {
            'status': 'failure',
            'data': data
        }
        assert status_code == 400
