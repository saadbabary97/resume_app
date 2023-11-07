from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/test_app/', include('test_app.urls')),
    path('api/media_file/', include('media_file.urls')),
]
