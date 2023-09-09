from django.urls import path

from assets_monitoring import views

urlpatterns = [
    path('register/', views.ownership_register, name='ownership_register'),
    path('delete/<str:ticker>/', views.ownership_delete, name='ownership_delete'),
    path('', views.ownership_list, name='ownership_list'),
]
