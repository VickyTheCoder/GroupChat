from django_filters import FilterSet
from django.contrib.auth.models import User, Group

class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']

class GroupFilter(FilterSet):
    class Meta:
        model = Group
        fields = ['name']