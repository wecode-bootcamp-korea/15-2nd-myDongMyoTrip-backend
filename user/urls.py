from django.urls import path
from .           import views

# Serializer/APIView
urlpatterns = [
    path('/signup', views.UserSignUpView.as_view()),
    path('/signin', views.UserSignInView.as_view())
]


# Form class
#urlpatterns = [
#    path('/signup', signup, name='signup'),
#    path('/signin', signin, name='signin'),
#]
#
# Project
#from user.views   import (
#    SignUpView,
#    ActivateView,
#    SignInView,
#    KakaoSignInView
#    )
#
#urlpatterns = [
#    path('/sign-up', SignUpView.as_view()),
#    path('/activate/<str:uidb64>/<str:access_token>', ActivateView.as_view()),
#    path('/sign-in', SignInView.as_view()),
#    path('/sign-in/kakao', KakaoSignInView.as_view()),
#]

