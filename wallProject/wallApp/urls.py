from django.urls import path
from .import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('wall', views.success),
    path('logout', views.logout),
    path('postm', views.post_message),
    path('postc', views.post_comment),
    path('message/<int:msg_id>/delete', views.delete_message),

]
