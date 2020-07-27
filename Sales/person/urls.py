from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'person'

urlpatterns = [    
    path('company-create/', views.company_create, name = 'url_company_create'),
    path('companies/', views.companies_list, name='url_companies_list'),
    path('company/<slug:slug>/detail', views.company_detail, name='url_company_detail'),
    path('company/<slug:slug>/edit', views.company_edit, name='url_company_edit'),
    path('company/<slug:slug>/delete', views.company_delete, name='url_company_delete'),
    path('company/delete_all/', views.company_delete_all, name='url_company_delete_all'),
    path('company/translate-js/', views.company_translate_js, name='url_company_translate_js'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)