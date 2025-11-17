from django.urls import path
from . import views

app_name = 'dashboard_api'

urlpatterns = [
    # Page data endpoints
    path('home/', views.home_data, name='home_data'),
    path('franchise/', views.franchise_data, name='franchise_data'),
    path('packages-page/', views.packages_data, name='packages_data'),
    path('contact/', views.contact_data, name='contact_data'),
    
    # Car wash packages endpoints
    path('car-wash-packages/', views.car_wash_packages, name='car_wash_packages'),
    path('car-wash-packages/<int:package_id>/', views.package_detail, name='package_detail'),
    
    # Gallery endpoints
    path('gallery/', views.gallery_items, name='gallery_items'),
]