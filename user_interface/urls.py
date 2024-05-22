from django.contrib import admin
from django.urls import path
from user_interface.UI.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name= 'home')

]
