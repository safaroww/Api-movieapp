from django.urls import path
from . import views
from rest_framework.authtoken import views as auth_views


urlpatterns = [
    path('directors/', views.DirectorListAV.as_view(), name='director-list'),
    path('directors/<int:pk>/', views.DirectorDetailAV.as_view(), name='director-detail'),
    # path('customer-login/', auth_views.obtain_auth_token, name='customer-login')
    path('customer-login/', views.customer_login, name='customer-login'),
    path('customer-register/', views.customer_register, name='customer-register'),
    path('director-login/', views.director_login, name='director-login'),
    path('director-register/', views.director_register, name='director-register'),
    path('admin-login/', views.admin_login, name='admin-login')
]
