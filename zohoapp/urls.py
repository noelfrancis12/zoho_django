from django.urls import path,include
from.import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('base', views.base, name='base'),
    path('logout', views.logout, name='logout'),
    path('view_profile', views.view_profile, name='view_profile'),
    path('edit_profile/<pk>', views.edit_profile, name='edit_profile'),
]