from django.urls import path
from accommodation.views  import AccommodationDetailView, AccommodationListView

urlpatterns=[
    path('/<int:accommodation_id>', AccommodationDetailView.as_view()),
    path('/list', AccommodationListView.as_view())
]