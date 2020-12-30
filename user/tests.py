import json, bcrypt, jwt, re, requests, unittest

from django.test   import TestCase, Client
from .models       import User, SocialPlatform
from unittest.mock import patch, MagicMock

class UserSignUpTest(TestCase):
    def setUp(self):
        client = Client()
        User.objects.create(
            name                = 'Wecode Lee',
            email               = 'wecode@gmail.com',
            password            = bcrypt.hashpw('wecode123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            is_location_agreed  = False,
            is_promotion_agreed = False,
            is_active           = False,
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_signupview_post_success(self):

        user = {
            'name'                : 'Mecode Lee',
            'email'               : 'mecode@gmail.com',
            'password'            : 'mecode123',
            'is_location_agreed'  : False,
            'is_promotion_agreed' : False,
            'is_active'           : False,
        }
        response = self.client.post('/user/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message': 'SUCCESS'})

    def test_signupview_post_user_already_exists(self):

        user = {
            'name'                : 'Wecode Lee',
            'email'               : 'wecode@gmail.com',
            'password'            : 'wecode123',
            'is_location_agreed'  : False,
            'is_promotion_agreed' : False,
            'is_active'           : False,
        }
        response = self.client.post('/user/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'USER_ALREADY_EXISTS'})

    def test_signupview_post_invalid_email(self):

        user = {
            'name'                : 'Nacode Lee',
            'email'               : 'nacodegmail.com',
            'password'            : 'nacode123',
            'is_location_agreed'  : False,
            'is_promotion_agreed' : False,
            'is_active'           : False,
        }
        response = self.client.post('/user/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_EMAIL'})

    def test_signupview_post_invalid_password(self):

        user = {
            'name'                : 'Youcode Lee',
            'email'               : 'youcode@gmail.com',
            'password'            : 'youcode',
            'is_location_agreed'  : False,
            'is_promotion_agreed' : False,
            'is_active'           : False,
        }
        response = self.client.post('/user/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'INVALID_PASSWORD'})

    def test_signupview_post_key_error(self):

        user = {
            'name'                : 'Uscode Lee',
            'email'               : 'uscode@gmail.com',
            'password'            : 'uscode123',
        }
        response = self.client.post('/user/sign-up', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

class UserSignInTest(TestCase):
    def setUp(self):
        client = Client()
        User.objects.create(
            email    = 'wecode@gmail.com',
            password = bcrypt.hashpw('wecode123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        )

        SocialPlatform.objects.create(platform='kakao')

    def tearDown(self):
        User.objects.all().delete()
        SocialPlatform.objects.get(platform='kakao').delete()
    
    def test_signinview_post_success(self):

        user = {
            'email'               : 'wecode@gmail.com',
            'password'            : 'wecode123',
        }
        response = self.client.post('/user/sign-in', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'SUCCESS', 'access_token': response.json()['access_token']})

    def test_signinview_post_invalid_password(self):

        user = {
            'email'               : 'wecode@gmail.com',
            'password'            : 'wecode321',
        }
        response = self.client.post('/user/sign-in', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message': 'INVALID_PASSWORD'})

    def test_signinview_post_user_does_not_exist(self):

        user = {
            'email'               : 'mecode@gmail.com',
            'password'            : 'wecode123',
        }
        response = self.client.post('/user/sign-in', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'USER_DOES_NOT_EXIST'})


    def test_signinview_post_key_error(self):

        user = {
            'email'               : 'wecode@gmail.com',
        }
        response = self.client.post('/user/sign-in', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message': 'KEY_ERROR'})

    @patch('user.views.requests')
    def test_kakao_sign_in_success(self, mocked_request):
        class KakaoResponse:
            def json(self):
                return {'kakao_account': {
                            'id'        : '12345',
                            'profile'   : {'nickname': 'test_user'},
                            'email'     : 'test@gmail.com'
                            }
                        }

        mocked_request.get = MagicMock(return_value = KakaoResponse())

        header = {'HTTP_Authorization': 'access_token'}

        response = self.client.get('/user/sign-in/kakao', content_type='application/json', **header)

        self.assertEqual(response.status_code, 200)

    @patch('user.views.requests')
    def test_kakao_sign_in_invalid_token(self, mocked_request):
        class KakaoResponse:
            def json(self):
                 return {'kakao_account': {
                            'id'        : '12345',
                            'profile'   : {'nickname': 'test_user'},
                            'email'     : 'test@gmail.com'
                            }
                        }

        mocked_request.get = MagicMock(return_value = KakaoResponse())

        header = {'HTTP_Authorization': 'invalid_token'}

        response = self.client.get('/user/sign-in/kakao', content_type='application/json', **header)

    @patch('user.views.requests')
    def test_kakao_sign_in_key_error(self, mocked_request):
        class KakaoResponse:
            def json(self):
                 return {
                         'message': 'KEY_ERROR',
                         'kakao_account': {
                            'id'        : '12345',
                            'profile'   : {'nickname': 'test_user'},
                            }
                        }

        mocked_request.get = MagicMock(return_value = KakaoResponse())

        header = {'HTTP_Authorization': 'access_token'}
 
        response = self.client.get('/user/sign-in/kakao', content_type='application/json', **header)
