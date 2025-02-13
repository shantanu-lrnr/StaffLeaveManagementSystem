from django.urls import path,include
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("home/",views.home,name = "home"),
    path("login/",views.login_view,name = "login"),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', views.password_reset_confirm_view,
         name='password_reset_confirm'),
]

