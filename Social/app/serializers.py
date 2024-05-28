from rest_framework import serializers, validators
from .models import *
from django.contrib.auth.models import User

class RegisterSerial(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self):
        # account = User(first_name=self.validated_data['first_name'], 
        #                last_name=self.validated_data['last_name'],
        #                username=self.validated_data['username'], 
        #                email=self.validated_data['email'])
        account = User(**self.validated_data)
        account.set_password(self.validated_data['password'])
        account.save()
        return account
        
    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Password and Confirm Password should be same.")
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email Already Registered Use new email or Login")
        return data

class PostSerial(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'image', 'caption', 'tags', 'user']

class CommentSerial(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'post', 'text']

class LikeSerial(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['user', 'post']
        validators = [
            validators.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'post'),
                message=("Already Liked the post once")
            )
        ] 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
               
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