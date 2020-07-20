from django.urls import path
from . import views

app_name = 'person'

urlpatterns = [    
    path('company-create/', views.company_create, name = 'url_company_create'),
    path('companies/', views.companies_list, name='url_companies_list'),
    path('company/<int:pk>/detail', views.company_detail, name='url_company_detail'),
    path('company/<int:pk>/edit', views.company_edit, name='url_company_edit'),
    path('company/<int:pk>/delete', views.company_delete, name='url_company_delete'),
    path('company/delete_all/', views.company_delete_all, name='url_company_delete_all'),
    
]