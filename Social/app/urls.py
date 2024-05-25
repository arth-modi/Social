from django.urls import path,re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'post', Postview)
router.register(r'comment', Commentview)
router.register(r'like', Likeview)

urlpatterns = [
    path('register/',register_user, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', logout_user, name='logout'),
]