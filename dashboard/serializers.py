from rest_framework import serializers
from .models import FranchiseInstaller, HomePage, FranchisePage, PackagesPage, ContactPage, CarWashPackage, PackageInclude, GalleryItem, ServiceCategory

class PackageIncludeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageInclude
        fields = ['id', 'item_text', 'order']

class ServiceCategorySerializer(serializers.ModelSerializer):
    service_type_display = serializers.CharField(source='get_service_type_display', read_only=True)

    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'service_type', 'service_type_display']

class CarWashPackageSerializer(serializers.ModelSerializer):
    includes = PackageIncludeSerializer(many=True, read_only=True)
    category = ServiceCategorySerializer(read_only=True)
    
    class Meta:
        model = CarWashPackage
        fields = [
            'id', 'category', 'title', 'description', 'ideal_for', 
            'material', 'warranty', 'saloon_price', 'suv_price',
            'button_text', 'includes', 'is_active', 'created_at'
        ]

class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePage
        fields = ['id', 'title', 'description', 'image', 'video', 'media_type']

class FranchisePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FranchisePage
        fields = ['id', 'title', 'description', 'image', 'video', 'media_type']

class PackagesPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackagesPage
        fields = ['id', 'title', 'description', 'image', 'video', 'media_type']

class ContactPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage
        fields = ['id', 'title', 'description', 'image', 'video', 'media_type']

class GalleryItemSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryItem
        fields = ['id', 'title', 'description', 'file', 'file_url', 'type', 'created_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
    


class FranchiseInstallerSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    banner_image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = FranchiseInstaller
        fields = [
            'id', 'name', 'email', 'phone_number', 'whatsapp_number', 
            'location', 'address', 'description', 'map_url',
            'shop_open_time', 'shop_close_time', 'image_url', 
            'banner_image_url', 'created_at'
        ]
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
    
    def get_banner_image_url(self, obj):
        request = self.context.get('request')
        if obj.banner_image and request:
            return request.build_absolute_uri(obj.banner_image.url)
        return None