from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('patients/', views.patient_list, name='patient_list'),
    path('patients/add/', views.patient_add, name='patient_add'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:pk>/edit/', views.patient_edit, name='patient_edit'),
    path('patients/<int:pk>/delete/', views.patient_delete, name='patient_delete'),

    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/add/', views.doctor_add, name='doctor_add'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:pk>/edit/', views.doctor_edit, name='doctor_edit'),
    path('doctors/<int:pk>/delete/', views.doctor_delete, name='doctor_delete'),

    path('device-data/', views.device_data_list, name='device_data_list'),
    path('device-data/upload/', views.device_data_upload, name='device_data_upload'),
    path('device-data/<int:pk>/delete/', views.device_data_delete, name='device_data_delete'),

    path('reports/', views.report_list, name='report_list'),
    path('reports/add/', views.report_add, name='report_add'),
    path('reports/<int:pk>/', views.report_detail, name='report_detail'),
    path('reports/<int:pk>/edit/', views.report_edit, name='report_edit'),
    path('reports/<int:pk>/delete/', views.report_delete, name='report_delete'),

    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.order_add, name='order_add'),
    path('orders/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/<int:pk>/edit/', views.order_edit, name='order_edit'),
    path('orders/<int:pk>/delete/', views.order_delete, name='order_delete'),
    path('orders/<int:pk>/result/', views.order_result_upload, name='order_result_upload'),

    path('emergency/', views.emergency_list, name='emergency_list'),
    path('emergency/add/', views.emergency_add, name='emergency_add'),

    path('admin-panel/users/', views.user_management, name='user_management'),
    path('admin-panel/users/<int:pk>/delete/', views.user_delete, name='user_delete'),
    path('download/<str:model_name>/<int:pk>/', views.download_file, name='download_file'),
]
