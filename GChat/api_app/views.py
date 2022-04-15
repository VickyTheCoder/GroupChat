from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status

from api_app import api
from .serializers import UserSerializer

class RegisterView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if request.data.get('is_admin_user','').lower() == "true":
                user.is_superuser = True
                
            user.save()

            auth_token = api.get_tokens_for_user(user)
            data = {'user': request.data, 'token': auth_token}
            
            return Response(data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)