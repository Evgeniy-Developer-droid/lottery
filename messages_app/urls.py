from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('', views.messages, name="messages"),

    path('api/get-contacts', api.get_contacts, name="api-get-contacts"),
    path('api/get-messages', api.get_messages, name="api-get-messages"),
    path('api/post-message', api.post_message, name="api-post-message"),
    path('api/read-messages', api.read_messages, name="api-read-messages"),
    path('api/create-dialog', api.create_dialog, name="api-create-dialog"),
]
