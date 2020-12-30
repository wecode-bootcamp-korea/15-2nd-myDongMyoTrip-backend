import json, bcrypt, jwt, re, requests

from django.views                   import View
from django.http                    import HttpResponse, JsonResponse
from django.shortcuts               import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http              import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail               import EmailMessage
from django.utils.encoding          import force_bytes, force_text

from my_settings                    import SECRET_KEY, ALGORITHM, EMAIL
from .models                        import User, SocialPlatform
from .utils                         import validate_email, validate_password
from .text                          import message

class SignUpView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message': 'USER_ALREADY_EXISTS'}, status=400)

            if not validate_email(data['email']):
                return JsonResponse({'message':'INVALID_EMAIL'}, status=400)

            if not validate_password(data['password']): 
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=400)

            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'),bcrypt.gensalt())

            user = User.objects.create(
                name                = data['name'],
                email               = data['email'],
                password            = hashed_password.decode('utf-8'),
                is_location_agreed  = data['is_location_agreed'],
                is_promotion_agreed = data['is_promotion_agreed'],
                is_active           = False
            )

            current_site = get_current_site(request)
            domain       = current_site.domain
            uidb64       = urlsafe_base64_encode(force_bytes(user.id))
            access_token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')
            message_data = message(domain, uidb64, access_token)
            mail_title   = 'myDongMyoTrip 회원가입을 위한 인증을 완료해주세요'
            mail_to      = data['email']
            email        = EmailMessage(mail_title, message_data, to=[mail_to])
            email.send()

            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)

class ActivateView(View):
    def get(self, request, uidb64, access_token):
        try:
            uid      = force_text(urlsafe_base64_decode(uidb64))
            user     = User.objects.get(pk=uid)
            user_dic = jwt.decode(access_token, SECRET_KEY, ALGORITHM)

            if user.id == user_dic["user"]:
                user.is_active = True
                user.save()
                return redirect(EMAIL['REDIRECT_PAGE'])

            return JsonResponse({'message': 'AUTH_FAIL'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
                password = data['password']

                if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    access_token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM)
                    return JsonResponse({'message': 'SUCCESS', 'access_token': access_token.decode('utf-8')}, status=200)

                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=401)

            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=400)

        except KeyError:
            return  JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except ValueError:
            return JsonResponse({'message': 'VALUE_ERROR'}, status=400)

class KakaoSignInView(View):
    def post(self, request):
        try:
            access_token   = request.headers.get('Authorization', None)
            headers        = {'Authorization': f'Bearer {access_token}'}
            url            = 'https://kapi.kakao.com/v2/user/me'
            response       = requests.get(url, headers=headers)
            user           = response.json()
            social_id      = user['id']
            email          = user['kakao_account']['email']
            name           = user['properties']['nickname'],
            
            if email:
                user, created = SocialPlatform.objects.get_or_create(
                    social_id           = social_id,
                    platform            = 'Kakao'
                )

                if created:
                    User(
                    email               = email,
                    name                = name,
                    is_location_agreed  = False,
                    is_promotion_agreed = False
                    ).save()

                access_token = jwt.encode({'user': user.id}, SECRET_KEY, ALGORITHM).decode('utf-8')

                return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=200)

            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)
