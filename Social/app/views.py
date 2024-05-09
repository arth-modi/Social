from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

# Create your views here.
class Index(View):
    def get(self, request):
        name = 'Arth'
        return render(request, 'index.html', {'name':name})