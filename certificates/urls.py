from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.employee_list, name='employee_list'),
    path('employee/<int:pk>/', views.employee_edit, name='employee_edit'),
    path('employee/new/', views.employee_new, name='employee_new'),
    path('employee/<int:pk>/delete/', views.employee_delete, name='employee_delete'),

] + statiс(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
