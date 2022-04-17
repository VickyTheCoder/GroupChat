from django.urls import path
from .views import RegisterView, LoginView
from .views import UserListCreateView, UserEditView
from .views import GroupListCreateView, GroupDeleteView
from .views import GroupUserAddView

app_name='api_app'

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('users/', UserListCreateView.as_view()),
    path('users/<str:pk>', UserEditView.as_view()),
    path('group/', GroupListCreateView.as_view()),
    path('group/delete/<str:pk>', GroupDeleteView.as_view()),
    path('group/add-user/', GroupUserAddView.as_view()),
]