from django_filters import FilterSet
from django.contrib.auth.models import User

class UserFilter(FilterSet):
    class Meta:
        model = User
        fields = ['first_name', 'last_name','email']