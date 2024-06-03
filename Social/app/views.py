from django.core.mail import EmailMessage
from rest_framework.throttling import UserRateThrottle
from django.conf import settings
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets, generics, exceptions, authentication
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes, throttle_classes

class Throttle(UserRateThrottle):
  rate = '100/day'

class Registerview(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    permission_classes=[AllowAny]  
    throttle_classes=[Throttle]
    serializer_class=RegisterSerializer
    
    # def post(self,request):
    #     email = EmailMessage("Welcome to Social Media App",f"Hi {request.data.get('first_name')}, thank you for registering in Social Media App.",
    #     settings.EMAIL_HOST_USER, [request.data.get('email')])
    #     serializer = RegisterSerializer(data=request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         email.send()
    #         serializer.save()
    #         return Response({'message': 'User Created', 'Data':serializer.data, 
    #                             'id': User.objects.get(username=request.data.get('username')).id}, 
    #                         status=status.HTTP_201_CREATED)

class LoginAuthentication(generics.CreateAPIView):
    permission_classes=[AllowAny]
    def create(self, request, *args, **kwargs):
        # Get the username and password
        username = request.data.get('username')
        password = request.data.get('password')
        user = None
        
        if not user:
            user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'username':username, 'token': token.key}, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class Logoutview(generics.DestroyAPIView):
    def destroy(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class Postview(viewsets.ModelViewSet):
    queryset = Post.objects.prefetch_related('post_comment', 'post_like').all()
    # serializer_class = PostSerializer
    throttle_classes = [Throttle]
    filterset_fields=['title', 'caption', 'tags', 'user']
    search_fields = ['title', 'tags']
    
    def get_serializer_class(self):
        if self.request.method=="GET":
            return PostListSerializer
        return PostCreateSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        # context['user'] = user
        context.update({'user': user})
        # print(context['user'])
        return context
    # def create(self, request, *args, **kwargs):
    #     user_id = Token.objects.get(key=request.auth.key).user_id
    #     # print(request.data.get('user'), user_id)
    #     if int(user_id) == int(request.data.get('user')):
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     else:
    #         return Response("Enter Valid User Id", status=status.HTTP_400_BAD_REQUEST)

class Commentview(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    throttle_classes = [Throttle]
    filterset_fields=['user', 'post', 'text']
    # def create(self, request, *args, **kwargs):
    #     user_id = Token.objects.get(key=request.auth.key).user_id
    #     # print(request.data.get('user'), user_id)
    #     if int(user_id) == int(request.data.get('user')):
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     else:
    #         return Response("Enter Valid User Id", status=status.HTTP_401_UNAUTHORIZED)

class Likeview(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filterset_fields=['user', 'post']
    # def create(self, request, *args, **kwargs):
    #     user_id = Token.objects.get(key=request.auth.key).user_id
    #     # print(request.data.get('user'), user_id)
    #     if int(user_id) == int(request.data.get('user')):
    #         serializer = self.get_serializer(data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         self.perform_create(serializer)
    #         headers = self.get_success_headers(serializer.data)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #     else:
    #         return Response("Enter Valid User Id", status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['DELETE',])
def remove_like(request):
    if request.method == 'DELETE':
        user_id = Token.objects.get(key=request.auth.key).user_id
        if int(user_id)== int(request.data.get('user')):
            if Like.objects.filter(user=request.data.get('user'), post=request.data.get('post')).exists():
                Like.objects.filter(user=request.data.get('user'), post=request.data.get('post')).delete()
                return Response({'message':'Unlike'},status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("Already didn't like the post")
        else:
            return Response("Not a Valid user Id", status=status.HTTP_401_UNAUTHORIZED)    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #     return super().perform_create(serializer)
    
    