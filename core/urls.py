from django.urls import path
from .views import SongCreateView

urlpatterns = [
    path('generate-song/', SongCreateView.as_view(), name='generate-song'),
]
