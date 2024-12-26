from django.urls import path

from . import views

app_name = 'tickets'

urlpatterns = [
    path('', views.index, name='index'),
    path('destinations/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path(
        'profile/<slug:username>/',
        views.UserDetailView.as_view(),
        name='profile'
    ),
    path(
        'edit_profile/',
        views.UserUpdateView.as_view(),
        name='edit_profile'
    ),
]
