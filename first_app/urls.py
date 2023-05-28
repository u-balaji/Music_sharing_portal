from django.urls import path
from first_app import views

app_name = 'first_app'

urlpatterns = [
    path('register', views.register, name='register'),
    path('user-login', views.user_login, name='user-login'),
    path('upload',views.upload,name='upload')
]
