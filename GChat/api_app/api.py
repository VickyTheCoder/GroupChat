from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import Group
from .models import GroupMessages, GroupMessagesLikes

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

def create_group_message_like(request,group_message_id):
    result = False
    message = 'Error in liking group message'

    if GroupMessages.objects.filter(id=group_message_id).exists():
        group_message = GroupMessages.objects.filter(id=group_message_id).first()
        group_message_like = GroupMessagesLikes()
        group_message_like.liked_user = request.user
        group_message_like.group_message = group_message
        group_message_like.save()
        group_message.likes += 1
        group_message.save()
        result = True
        message = 'Group message liked successfully'
    return result,message,group_message