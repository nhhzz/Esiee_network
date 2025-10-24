from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('map/', include('maps.urls')),
    path('posts/', include('posts.urls')),
    path('events/', include('events.urls')),
    path('messages/', include('messages_app.urls')),
]
