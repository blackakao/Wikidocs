from urllib.parse import urlparse
from django.urls import URLPattern, path
from .import views

app_name = 'customer_list'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:Customer_Idx>/', views.modify, name='modify'),
    path('<int:Customer_Idx>/modify', views.modify_action, name='modify_action'),
    path('create/', views.create, name='create'),
    path('create_action/', views.create_action, name='create_action'),
    path('salary_update_excel/', views.salary_update_excel, name='salary_update_excel'),
    path('test/', views.test, name='test'),
]
