from django.urls import path
from accommodation.views  import AccommodationDetailView

urlpatterns=[
    path('/<int:accommodation_id>', AccommodationDetailView.as_view())
]