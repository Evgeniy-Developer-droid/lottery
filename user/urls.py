from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('tickets/', views.tickets_view, name="tickets"),
    path('catalog/', views.catalog, name="user-catalog"),
    path('new-lottery/', views.new_lottery, name="new-lottery"),
    path('view-lottery/<int:pk>', views.view_lottery, name="view-lottery"),
    path('settings/', views.settings, name="settings"),
    path('messages/', views.messages, name="messages"),
    path('user-detail/<int:pk>', views.user_detail, name="user-detail"),

    path('api/define-winners', api.define_winners, name="api-define-winners"),
    path('api/change-user-avatar', api.change_user_avatar, name="api-change-user-avatar"),
    path('api/change-user-data', api.change_user_data, name="api-change-user-data"),
    path('api/add-complain', api.add_complain, name="api-add-complain"),
    path('api/add-estimate', api.add_estimate, name="api-add-estimate"),

    #messages
    path('api/get-contacts', api.get_contacts, name="api-get-contacts"),
    path('api/get-messages', api.get_messages, name="api-get-messages"),
    path('api/post-message', api.post_message, name="api-post-message"),
]