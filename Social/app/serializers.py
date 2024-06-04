from rest_framework import serializers, validators
from .models import *
# from django.contrib.auth.models import User
# from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='get_full_name')

    class Meta:
        model = CustomUser
        exclude = ['password','is_staff', 'is_active', 'user_permissions', 'groups', 'is_superuser', 'last_login', 'first_name', 'last_name']
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True, write_only = True)
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email','mobile','password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self):
        # account = CustomUser(**self.validated_data)
        account = CustomUser(first_name=self.validated_data['first_name'],
                             last_name=self.validated_data['last_name'],
                             mobile=self.validated_data['mobile'],
                             username=self.validated_data['username'], 
                             email=self.validated_data['email'],)
        email = EmailMessage("Welcome to Social Media App",
                             f"Hi {self.validated_data['first_name']}, thank you for registering in Social Media App.",
                            settings.EMAIL_HOST_USER, [self.validated_data['email']])
        account.set_password(self.validated_data['password'])
        account.save()
        email.send()
        return account
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password and Confirm Password should be same.")
        
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email Already Registered Use new email or Login")
        return data

class PostListSerializer(serializers.ModelSerializer):
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    user = UserSerializer()
    
    class Meta:
        model = Post
        fields = ['title', 'image', 'caption', 'tags', 'user', 'comment_count', 'like_count']
    
    def get_comment_count(self, obj):
        return obj.post_comment.count()
    
    def get_like_count(self, obj):
        return obj.post_like.count()       
    
class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ['title', 'image', 'caption', 'tags', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        # print(validated_data)
        # print(self.context)
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'text', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        # print(validated_data)
        # print(self.context)
        return super().create(validated_data)

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['post', 'user']
        validators = [
            validators.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'post'),
                message=("Already Liked the post once")
            )
        ] 
        
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return super().create(validated_data)   
    
    
    # def to_internal_value(self, data):
    #     user = Token.objects.get(key=self.context["request"].auth.key).user
    #     mutable_data = data.copy()
    #     mutable_data['user'] = user.id
    #     return super().to_internal_value(mutable_data)  
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
               
    # def create(self, request):
    #     user = request.user
    #     post_id = request.data.get('post')
    #     if Like.objects.filter(user=user, post_id=post_id).exists():
    #         return serializers.ValidationError("Already Liked the Post Once")
    #     return super().create(request)
    
    # def create(self, validated_data):
        
    #     user = self.context['request'].user
    #     post = validated_data.get('post')
    #     # context ={'user':user,'post':post}
    #     if Like.objects.filter(user=user,post=post).exists():
    #         return serializers.ValidationError("Already Liked")
    #     like = Like.objects.create(user=user, post=post)
    #     return like