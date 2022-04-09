from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('tickets/', views.tickets_view, name="tickets"),
    path('catalog/', views.catalog, name="user-catalog"),
    path('new-lottery/', views.new_lottery, name="new-lottery"),
    path('view-lottery/<int:pk>', views.view_lottery, name="view-lottery"),
    path('settings/', views.settings, name="settings"),
    path('user-detail/<int:pk>', views.user_detail, name="user-detail"),

    path('api/define-winners', api.define_winners, name="api-define-winners"),
]