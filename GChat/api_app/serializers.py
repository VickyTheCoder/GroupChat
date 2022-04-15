from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=65,write_only=True)
    email = serializers.EmailField(max_length=100)
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100,required=False)
    user_id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password','user_id', ]

    def validate(self, data):
        email = data.get('email','')
        if email:
            if self.instance:
                user = User.objects.filter(email=data.get('email')).exclude(id=self.instance.id)
            else:
                user = User.objects.filter(email=data.get('email'))
            if user:
                raise serializers.ValidationError("Email Already exists.Please give different email.")
        return data
    
    def get_user_id(self, data):
        return data.id

    def validate_password(self, value):
        return make_password(value)

    def save(self, *args, **kwargs):
        if self.instance:
            user = User.objects.filter(id=self.instance.id).first()
        else:
            user = User()
        user.username = self.validated_data.get('email')
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.email = self.validated_data.get('email')
        user.password = self.validated_data.get('password')
        return user