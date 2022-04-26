from django.urls import path, re_path
from . import views
from . import api

urlpatterns = [
    path('tickets/', views.tickets_view, name="tickets"),
    path('catalog/', views.catalog, name="user-catalog"),
    path('new-lottery/', views.new_lottery, name="new-lottery"),
    path('view-lottery/<int:pk>', views.view_lottery, name="view-lottery"),
    path('settings/', views.settings_, name="settings"),
    path('user-detail/<int:pk>', views.user_detail, name="user-detail"),
    path('password-reset/', views.password_reset, name="password-reset"),
    path('password-reset/done/', views.password_reset_done, name="password-reset-done"),
    re_path(r'^password-reset/confirm/(?P<uidb64>[\dA-Za-z_\-]+)/(?P<token>[\dA-Za-z]{1,13}-[\dA-Za-z]{1,100})/$',
            views.password_reset_confirm, name="password-reset-confirm"),
    path('password-reset/complete/', views.password_reset_complete, name="password-reset-complete"),

    path('api/define-winners', api.define_winners, name="api-define-winners"),
    path('api/change-user-avatar', api.change_user_avatar, name="api-change-user-avatar"),
    path('api/change-user-data', api.change_user_data, name="api-change-user-data"),
    path('api/add-complain', api.add_complain, name="api-add-complain"),
    path('api/add-estimate', api.add_estimate, name="api-add-estimate"),
]