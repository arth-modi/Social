from django.shortcuts import render
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
        serializer = RegisterSerial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message': 'User Created', 'Data':serializer.data}, status=status.HTTP_201_CREATED)
        
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
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

class Commentview(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerial
class Likeview(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerial
    
    def create(self, request):
        user = request.user
        post_id = request.data.get('post')
        
        if Like.objects.filter(user=user, post_id=post_id).exists():
            
            return Response("Already Liked the Post Once", status=status.HTTP_400_BAD_REQUEST)
                
        return super().create(request)  
    
    