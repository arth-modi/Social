from rest_framework.throttling import UserRateThrottle
from django.conf import settings
from .serializers import *
from .models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets, generics, exceptions, authentication, filters, serializers
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import api_view, permission_classes, throttle_classes, action
from .pagination import myPagination
from .filters import HasImageFilterBackend

class Throttle(UserRateThrottle):
  rate = '100/day'
class Registerview(generics.CreateAPIView):
    queryset=CustomUser.objects.all()
    permission_classes=[AllowAny]  
    throttle_classes=[Throttle]
    serializer_class=RegisterSerializer

class LoginAuthentication(generics.CreateAPIView):
    permission_classes=[AllowAny]
    def create(self, request, *args, **kwargs):

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
    throttle_classes = [Throttle]
    pagination_class=myPagination
    filter_backends=[HasImageFilterBackend, DjangoFilterBackend, filters.SearchFilter]
    filterset_fields=['title', 'caption', 'tags', 'user']
    search_fields = ['title', 'tags']
    
    def get_serializer_class(self):
        if self.action in ["listall", "retrieve", "list"]:
            return PostListSerializer
        return PostSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        context.update({'user': user})
        return context
    
    @action(detail=False, methods=['get'])
    def listall(self, request):
        queryset = Post.objects.all().order_by('id')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class Commentview(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    throttle_classes = [Throttle]
    filterset_fields=['user', 'post', 'text']
    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = Token.objects.get(key=self.request.auth.key).user
        context.update({'user': user})
        # print(context)
        return context
class Likeview(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filterset_fields=['user', 'post']
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     user = Token.objects.get(key=self.request.auth.key).user.id
    #     context.update({'user': user})
    #     # print(context)
    #     return context     
    
@api_view(['DELETE',])
def remove_like(request):
    if request.method == 'DELETE':
        user_id = int(Token.objects.get(key=request.auth.key).user_id)
        if Like.objects.filter(user=user_id, post=request.data.get('post')).exists():
            Like.objects.filter(user=user_id, post=request.data.get('post')).delete()
            return Response({'message':'Unlike'},status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Already didn't like the post")   
