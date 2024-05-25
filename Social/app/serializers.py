from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class RegisterSerial(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','password', 'confirm_password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self):
        account = User(first_name=self.validated_data['first_name'], 
                       last_name=self.validated_data['last_name'],
                       username=self.validated_data['username'], 
                       email=self.validated_data['email'])
        
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
        fields = "__all__"

class CommentSerial(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"

class LikeSerial(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"