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
    
    #Department
    path('company-departments/<slug:company_pk>/', views.company_departments, name='url_company_departments'),
    path('department-create/<slug:company_pk>/', views.department_create, name = 'url_department_create'),        
    path('department/<slug:slug>/detail', views.department_detail, name='url_department_detail'),
    path('department/<slug:slug>/edit', views.department_edit, name='url_department_edit'),
    path('department/<slug:slug>/delete', views.department_delete, name='url_department_delete'),    

    # path('department-position/<slug:slug>/', views.department_positions, name='url_department_positions'),
    # path('department-position-people/<slug:slug>/', views.position_people, name='url_position_people'),
    
    #Position    
    path('position-create/<slug:department_pk>/', views.position_create, name = 'url_position_create'),
    
    #Person            
    path('people/', views.people_list, name='url_people_list'),
    path('person-create-user/', views.create_user_and_person, name = 'url_create_user_and_person'),
    path('person/<slug:slug>/detail', views.person_detail, name='url_person_detail'),
    path('person/<slug:slug>/edit', views.person_edit, name='url_person_edit'),
    path('person/<slug:slug>/deactive', views.person_deactive, name='url_person_deactive'),
    path('person/<slug:slug>/delete', views.person_delete, name='url_person_delete'),
    path('person/delete_all/', views.person_delete_all, name='url_person_delete_all'),   

    # URL PARA TRADUZIR O DATATABLES. USO GERAL
    path('person/translate-js/', views.translate_datables_js, name='url_translate_datables_js'),

    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)