from django.urls import path
from . import views

urlpatterns = [
    path('', views.quotation_list, name='quotation_list'),
    path('create/', views.quotation_create, name='quotation_create'),
    path('view/<int:pk>/', views.quotation_view, name='quotation_view'),
    path('template/<int:template_id>/items/', views.load_template_items, name='load_template_items'),
    path('pdf/<int:pk>/', views.quotation_pdf, name='quotation_pdf'),
]
