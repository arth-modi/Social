from django.urls import path,re_path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'posts', Postview)
router.register(r'comments', Commentview)
router.register(r'like', Likeview)

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', obtain_auth_token, name='login'),
    path('logout/', logout_user, name='logout'),
    path('unlike/', remove_like, name='unlike'),
    path('', include(router.urls)),
]