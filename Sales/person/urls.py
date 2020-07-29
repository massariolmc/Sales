from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'person'

urlpatterns = [
    #Company    
    path('company-create/', views.company_create, name = 'url_company_create'),
    path('companies/', views.companies_list, name='url_companies_list'),
    path('company/<slug:slug>/detail', views.company_detail, name='url_company_detail'),
    path('company/<slug:slug>/edit', views.company_edit, name='url_company_edit'),
    path('company/<slug:slug>/delete', views.company_delete, name='url_company_delete'),
    path('company/delete_all/', views.company_delete_all, name='url_company_delete_all'),
    path('company/translate-js/', views.company_translate_js, name='url_company_translate_js'),
    #Department
    path('department-create/', views.department_create, name = 'url_department_create'),
    path('departments/', views.departments_list, name='url_departments_list'),
    path('department/<slug:slug>/detail', views.department_detail, name='url_department_detail'),
    path('department/<slug:slug>/edit', views.department_edit, name='url_department_edit'),
    path('department/<slug:slug>/delete', views.department_delete, name='url_department_delete'),
    path('department/delete_all/', views.department_delete_all, name='url_department_delete_all'),
    path('department/translate-js/', views.department_translate_js, name='url_department_translate_js'),
    #PersonType    
    path('person_type-create/', views.person_type_create, name = 'url_person_type_create'),
    path('person_types/', views.person_types_list, name='url_person_types_list'),
    path('person_type/<slug:slug>/detail', views.person_type_detail, name='url_person_type_detail'),
    path('person_type/<slug:slug>/edit', views.person_type_edit, name='url_person_type_edit'),
    path('person_type/<slug:slug>/delete', views.person_type_delete, name='url_person_type_delete'),
    path('person_type/delete_all/', views.person_type_delete_all, name='url_person_type_delete_all'),
    path('person_type/translate-js/', views.person_type_translate_js, name='url_person_type_translate_js'),
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)