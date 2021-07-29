from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # paths to our application
    path('app/', include('App.urls')),
]
