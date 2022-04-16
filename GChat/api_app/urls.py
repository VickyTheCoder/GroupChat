from django.urls import path
from .views import RegisterView, LoginView, UserListCreateView

app_name='api_app'

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UserListCreateView.as_view()),
]