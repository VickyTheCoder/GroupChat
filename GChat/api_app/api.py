from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from .models import GroupMessages

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def create_group_message(request,group):
    result = False
    message = 'Error in creating group message'
    if Group.objects.filter(id=group).exists():
        group = Group.objects.filter(id=group).first()
        group_message = GroupMessages()
        group_message.user = request.user
        group_message.group = group
        group_message.text = request.data.get('text','')
        group_message.save()
        result = True
        message = 'Group message created successfully'
    return result,message,group_message