from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.logout_, name="logout"),
    path('signup/', views.signup, name="signup"),
    path('catalog/', views.catalog, name="catalog"),
    path('privacy/', views.privacy, name="privacy"),
    path('contact-us/', views.contact_us, name="contact_us"),
    path('single/<int:pk>', views.single, name="single"),

    re_path(r'^activate/(?P<uidb64>[\dA-Za-z_\-]+)/(?P<token>[\dA-Za-z]{1,13}-[\dA-Za-z]{1,100})/$',
        views.activate, name='activate'),
]