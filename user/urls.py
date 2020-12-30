from django.urls  import path
from user.views   import (
    SignUpView,
    ActivateView,
    SignInView,
    KakaoSignInView
    )

urlpatterns = [
    path('/sign-up', SignUpView.as_view()),
    path('/activate/<str:uidb64>/<str:access_token>', ActivateView.as_view()),
    path('/sign-in', SignInView.as_view()),
    path('/sign-in/kakao', KakaoSignInView.as_view()),
]

