from django.db import models
from django.contrib.auth.models import User, Group

MESSAGE_TYPE_CHOICES = (('TEXT','Text'),('MEDIA', 'Media'))
DATAMODE_CHOICES = (('A','Active'),('I', 'Inactive'),('D','Deleted'))

class GroupMessages(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message_type = models.CharField(max_length=32, default='TEXT', choices=MESSAGE_TYPE_CHOICES) #TEXT/MEDIA
    text =  models.TextField(blank=True,null=True)
    media_url = models.URLField(blank=True, null=True)
    is_edited = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=10, default='A', choices=DATAMODE_CHOICES)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'GroupMessages'
        verbose_name_plural = 'GroupMessages'
        db_table = 'group_messages'

class GroupMessagesLikes(models.Model):
    liked_user = models.ForeignKey(User, on_delete=models.CASCADE)
    group_message = models.ForeignKey(GroupMessages, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    datamode = models.CharField(max_length=10, default='A', choices=DATAMODE_CHOICES)

    def __str__(self):
        return self.liked_user

    class Meta:
        verbose_name = 'GroupMessagesLikes'
        verbose_name_plural = 'GroupMessagesLikes'
        db_table = 'group_message_likes'