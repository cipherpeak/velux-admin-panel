from django.urls import path, include

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('update-card/', views.update_card, name='update_card'),  
    path('packages/', views.package_page, name='packages'),
    path('create-package/', views.create_package, name='create_package'),
    path('update-package/<int:package_id>/', views.update_package, name='update_package'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('gallery/add/', views.add_gallery_item, name='add_gallery_item'),
    path('gallery/add/image/', views.add_image, name='add_image'),
    path('gallery/add/video/', views.add_video, name='add_video'),
    path('gallery/delete/<int:item_id>/', views.delete_gallery_item, name='delete_gallery_item'),
    path('gallery/api/items/', views.get_gallery_items, name='get_gallery_items'),

    path('api/', include('dashboard.api.urls')),


]