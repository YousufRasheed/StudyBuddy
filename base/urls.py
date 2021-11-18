from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView, name="login"),
    path('register/', views.register_request, name="register"),
    path('logout/', views.LogoutView, name="logout"),
    path('', views.home, name="home"),
    path('room/<str:pk>', views.room, name="room"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>', views.deleteRoom, name="delete-room"),
    path('delete-msg/<str:pk>', views.deletemsg, name="delete-message"),
    path('profile/<str:pk>', views.profile, name='user-profile'),
]