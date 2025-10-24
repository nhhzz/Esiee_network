from django.shortcuts import render

def index(request):
    return render(request,'messages_app/index.html')
