import jwt, json, re

from django.http import JsonResponse

from my_settings import SECRET_KEY, ALGORITHM
from .models     import User


def authorize_user(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user         = User.objects.get(id=payload['user'])
            request.user = user

            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=403)

        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=401)

    return wrapper

def validate_email(email):
    REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    return re.match(REGEX_EMAIL, email)

def validate_password(password):
    REGEX_PASSWORD_1 = '^(?=.*[0-9])(?=.*[a-zA-Z]).{6,15}$'
    REGEX_PASSWORD_2 = '^(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{6,15}$'
    REGEX_PASSWORD_3 = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+]).{6,15}$'
    REGEX_PASSWORD_4 = '^(?=.*[0-9])(?=.*[!@#$%^&*()_+])(?=.*[a-zA-Z]).{6,15}$'

    return re.match(REGEX_PASSWORD_1, password) or re.match(REGEX_PASSWORD_2, password) \
        or re.match(REGEX_PASSWORD_3, password) or re.match(REGEX_PASSWORD_4, password)
