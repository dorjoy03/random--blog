from django.urls import path, include

from .views import signup

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', signup, name='signup'),
]
