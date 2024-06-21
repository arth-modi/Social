from rest_framework import serializers, validators
from .models import *
from rest_framework.authtoken.models import Token
from django.core.mail import EmailMessage
from django.conf import settings
from app.task import send_email

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
        account = CustomUser(first_name=self.validated_data['first_name'],
                             last_name=self.validated_data['last_name'],
                             mobile=self.validated_data['mobile'],
                             username=self.validated_data['username'], 
                             email=self.validated_data['email'],)
        # email = EmailMessage("Welcome to Social Media App",
        #                      f"Hi {self.validated_data['first_name']}, thank you for registering in Social Media App.",
        #                     settings.EMAIL_HOST_USER, [self.validated_data['email']])
        account.set_password(self.validated_data['password'])
        send_email.delay(self.validated_data['first_name'], self.validated_data['email'])
        account.save()
        # email.send()
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
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Post
        fields = ['title', 'image', 'caption', 'tags', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
        return super().create(validated_data)

class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=150)
    image = serializers.ImageField()
    caption = serializers.CharField()
    tags = serializers.CharField()
    user = serializers.CharField(required=False)
    
    def create(self, validated_data):
        return Post.objects.create(title = validated_data['title'],
                    image = validated_data['image'],
                    caption = validated_data['caption'],
                    tags = validated_data['tags'],
                    user = self.context.get('user')
                    )

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.image = validated_data.get('image', instance.image)
        instance.caption = validated_data.get('caption', instance.caption)
        instance.tags = validated_data.get('tags', instance.tags)
        instance.user = self.context.get('user')
        instance.save()
        return instance
    
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['post', 'text', 'user']
    
    def create(self, validated_data):
        validated_data['user'] = self.context.get('user')
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
        
    # def create(self, validated_data):
    #     validated_data['user'] = self.context.get('user')
    #     return super().create(validated_data)   
      
    def to_internal_value(self, data):
        user = Token.objects.get(key=self.context["request"].auth.key).user
        mutable_data = data.copy()
        mutable_data['user'] = user.id
        return super().to_internal_value(mutable_data)  