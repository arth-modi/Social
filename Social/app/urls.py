from django.urls import path, include
from . import views
from app.views import Index

urlpatterns = [
    path('', Index.as_view(), name='index'),    
]

