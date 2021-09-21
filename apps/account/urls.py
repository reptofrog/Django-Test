from django.urls import path

from . import views


app_name = 'account'

urlpatterns = [
    path('', views.profile_view, name="profile"),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
]
