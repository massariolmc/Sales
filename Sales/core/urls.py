from django.urls import path
from . import views

app_name = 'signup'

urlpatterns = [
    path('home', views.home, name='home'),
    path('signup-create/', views.signup, name = 'url_signup_create'),
    path('signup/', views.signup_list, name='url_signup_list'),
    path('<int:pk>/delete', views.signup_delete, name='url_signup_delete'),
    path('<int:pk>/detail', views.signup_detail, name='url_signup_detail'),
    path('<int:pk>/edit', views.signup_edit, name='url_signup_edit'),
]