from django.urls import path,re_path, include
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'posts', Postview)
router.register(r'comments', Commentview)
router.register(r'like', Likeview)

urlpatterns = [
    path('register/', Registerview.as_view(), name='register'),
    path('login/', LoginAuthentication.as_view(), name='login'),
    path('logout/', Logoutview.as_view(), name='logout'),
    path('unlike/', remove_like, name='unlike'),
    path('', include(router.urls)),
]