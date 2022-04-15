from django.urls import path
from .views import RegisterView

app_name='api_app'

urlpatterns = [
    path('register/', RegisterView.as_view()),
]