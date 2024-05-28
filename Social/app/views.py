from django.shortcuts import render
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == "POST":
        email = EmailMessage("Welcome to Social Media App",f"Hi {request.data.get('first_name')}, thank you for registering in Social Media App.",
        settings.EMAIL_HOST_USER, [request.data.get('email')])
        serializer = RegisterSerial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email.send()
            # send_mail( subject, message, from_email, recipient_list )
            serializer.save()
            return Response({'message': 'User Created', 'Data':serializer.data}, status=status.HTTP_201_CREATED)
        
@api_view(['POST'])
def logout_user(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class Postview(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerial
    filterset_fields=['title', 'caption', 'tags', 'user']
    search_fields = ['title', 'tags']

class Commentview(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerial
    filterset_fields=['user', 'post', 'text']

class Likeview(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerial
    filterset_fields=['user', 'post']
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    #     return super().perform_create(serializer)
    
    