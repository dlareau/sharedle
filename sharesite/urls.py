from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input/', views.input, name='input'),
    path('groups/', views.groups, name='groups'),
    path('group/<uuid:group_id>/', views.group, name='group'),
    path('login/async/', views.login_async, name='login_async'),
    path('profile/', views.update_profile, name='update_profile'),
    path('invite/<uuid:group_id>/<uuid:secret>/', views.invite, name='invite'),
]
