from django.urls    import include, path
from rest_framework import routers
from user           import views

router = routers.DefaultRouter()
#
urlpatterns = [
    path('', include(router.urls)),
    path('user', include('user.urls')),
    path('api_auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/rest_auth/', include('rest_auth.urls')),
]

