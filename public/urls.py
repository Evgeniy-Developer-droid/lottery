from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.logout_, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('catalog/', views.catalog, name="catalog"),
    path('single/<int:pk>', views.single, name="single"),
]