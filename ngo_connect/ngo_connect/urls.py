from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('base.urls')),
    path('base/', include('base.urls')),
    path('ngo/', include('ngo.urls')),
    path('donor/',include('donor.urls')),
    path('reciever/', include('reciever.urls')),
    path('chat/', include('chat.urls')),
]  
