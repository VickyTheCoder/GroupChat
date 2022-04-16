from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

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
        method = self.context.get('request').method
        if method == "POST" and user:
            raise serializers.ValidationError("Email Already exists.Please give different email.")
        elif method == "PUT" and not user:
            raise serializers.ValidationError("No user with such Email")
        return data
    
    def get_user_id(self, data):
        return data.id

    def validate_password(self, value):
        return make_password(value)

    def save(self, *args, **kwargs):
        method = self.context.get('request').method
        if method == "POST":
            user = User()
        else:
            user = User.objects.filter(email=self.validated_data.get('email')).first()
        user.username = self.validated_data.get('email')
        user.email = self.validated_data.get('email')
        user.first_name = self.validated_data.get('first_name')
        user.last_name = self.validated_data.get('last_name')
        user.password = self.validated_data.get('password')    
        return user

class LoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate(self, data):
        user = User.objects.filter(email=data['email'])
        if user:
            auth_user = authenticate(username=user.first().username, password=data['password'])
            if not auth_user:
                raise serializers.ValidationError("Please enter valid password.")
        else:
            raise serializers.ValidationError("There is no account in our system for this Email.")
        return data

