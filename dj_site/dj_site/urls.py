from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view, name= 'Home'),
    path('about/',views.about_view, name= 'About'),
    path('users/',include('users.urls'))
]
