from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status, permissions
from rest_framework_filters import backends
from rest_framework.filters import SearchFilter, OrderingFilter

from django.contrib.auth.models import User, Group

from api_app import api
from .serializers import UserSerializer, LoginSerializer
from .serializers import GroupSerializer, GroupUserAddSerializer
from .serializers import GroupMessageSerializer
from .models import GroupMessages
from .filters import UserFilter, GroupFilter

class RegisterView(GenericAPIView):
    serializer_class = UserSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if request.data.get('is_admin_user','').lower() == "true":
                user.is_superuser = True
            try:
                user.save()
            except Exception as e:
                return Response(f"Unable to add user: {e}", status=status.HTTP_400_BAD_REQUEST)
            auth_token = api.get_tokens_for_user(user)
            data = {'user': request.data, 'token': auth_token}
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(email=request.data.get('email')).first()
            auth_token = api.get_tokens_for_user(user)
            serializer = UserSerializer(user)
            data = {'user': serializer.data, 'token': auth_token}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class UserListCreateView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_class = UserFilter
    search_fields = ['first_name', 'last_name','email']
    filter_backends = [backends.RestFrameworkFilterBackend, SearchFilter, OrderingFilter]

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                if request.data.get('is_admin_user','').lower() == "true":
                    user.is_superuser = True
                user.save()
                data = {'message':'User created successfully' }
                return Response(data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(e, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserEditView(GenericAPIView):
    serializer_class = UserSerializer
    def put(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            auth_token = api.get_tokens_for_user(user)
            data = {'user': request.data, 'token': auth_token}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupListCreateView(ListCreateAPIView):
    serializer_class = GroupSerializer
    # permission_classes = [permissions.IsAuthenticated]
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_class = GroupFilter
    search_fields = ['name', ]
    filter_backends = [backends.RestFrameworkFilterBackend, SearchFilter, OrderingFilter]
    
    def get_queryset(self):
        return Group.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            data = {'message':'Group created successfully' }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupDeleteView(DestroyAPIView):
    permission_classes = [permissions.AllowAny]

    def destroy(self, request, *args, **kwargs):
        group = Group.objects.filter(name=self.kwargs['pk'])
        if group:
            group.delete()
        else:
            return Response("No Such Group", status=status.HTTP_400_BAD_REQUEST)
        data = {'message':'Group deleted successfully' }
        return Response(data, status=status.HTTP_200_OK)

class GroupUserAddView(GenericAPIView):
    serializer_class = GroupUserAddSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=request.data.get('email',''))
            group = Group.objects.get(name=request.data.get('group',''))
            group.user_set.add(user)
            data = {'message': 'Successfully added to the group'}
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupMessageListCreateView(ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    pagination_class = StandardResultsSetPagination
    serializer_class = GroupMessageSerializer

    def get_queryset(self):
        return GroupMessages.objects.filter(group=self.request.data.get('name', '')).order_by('-updated_on')

    def create(self, request, *args, **kwargs):
        group_id = self.kwargs['pk']
        result, message, group_message = api.create_group_message(request,group_id)
        data = {'message':message}
        if result:
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
 