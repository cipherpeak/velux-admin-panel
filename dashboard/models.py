from django.db import models
from django.core.validators import RegexValidator
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from django.db import models

class HomePage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, default="Home Services")
    description = models.TextField(default="Professional home maintenance and repair services to keep your living space comfortable and well-maintained throughout the year.")
    image = models.ImageField(upload_to='cards/', default='images/notes/home.jpg')
    video = models.FileField(upload_to='cards/videos/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Home Page Card"
        verbose_name_plural = "Home Page Card"

    def get_media_url(self):
        """Return the appropriate media URL based on media type"""
        if self.media_type == 'video' and self.video:
            return self.video.url
        return self.image.url
    
    def get_media_type(self):
        """Return the media type for template rendering"""
        return self.media_type

# Update other models similarly
class FranchisePage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, default="Franchise Opportunities")
    description = models.TextField(default="Join our growing network of franchises and be part of our success story.")
    image = models.ImageField(upload_to='cards/', default='images/notes/franchise.jpg')
    video = models.FileField(upload_to='cards/videos/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    updated_at = models.DateTimeField(auto_now=True)

class PackagesPage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, default="Our Packages")
    description = models.TextField(default="Explore our carefully crafted packages designed to meet your every need.")
    image = models.ImageField(upload_to='cards/', default='images/notes/packages.jpg')
    video = models.FileField(upload_to='cards/videos/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    updated_at = models.DateTimeField(auto_now=True)

class ContactPage(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    
    title = models.CharField(max_length=200, default="Get In Touch")
    description = models.TextField(default="Contact us for any inquiries or support. We're here to help you.")
    image = models.ImageField(upload_to='cards/', default='images/notes/contact.jpg')
    video = models.FileField(upload_to='cards/videos/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES, default='image')
    updated_at = models.DateTimeField(auto_now=True)


from django.db import models
from django.contrib.auth.models import User

class ServiceCategory(models.Model):
    SERVICE_CHOICES = [
        ('ppf', 'Paint Protection Film (PPF)'),
        ('window_tinting', 'Window Tinting'),
        ('borophene', 'Borophene Coating'),
        ('graphene', 'Graphene Coating'),
        ('ceramic', 'Ceramic Coating'),
        ('interior', 'Interior Detailing'),
        ('car_wash', 'Car Wash'),
    ]
    
    service_type = models.CharField(
        max_length=50, 
        choices=SERVICE_CHOICES, 
        default='wash'
    )
    name = models.CharField(
        max_length=100,
        help_text="Sub-category name (e.g., Glossy, Matte, Standard)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.name}"

class CarWashPackage(models.Model):
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='packages',
        null=True,
        blank=True
    )
    title = models.CharField(max_length=200, default="Essential Care")
    description = models.TextField(
        default="Perfect for maintaining your vehicle's appearance with professional exterior and interior care."
    )
    ideal_for = models.CharField(
        max_length=300, 
        default="Regular maintenance, monthly touch-ups"
    )
    material = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Material information if applicable"
    )
    warranty = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Warranty duration or terms"
    )
    saloon_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Price for Saloon/Sedan"
    )
    suv_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0.00,
        help_text="Price for SUV/4x4"
    )
    button_text = models.CharField(
        max_length=100, 
        default="Select Package"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Car Wash Package"
        verbose_name_plural = "Car Wash Packages"
    
    def __str__(self):
        return f"{self.category} - {self.title}"

class PackageInclude(models.Model):
    package = models.ForeignKey(
        CarWashPackage, 
        on_delete=models.CASCADE, 
        related_name='includes'
    )
    item_text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Package Include"
        verbose_name_plural = "Package Includes"
        ordering = ['order', 'id']
    
    def __str__(self):
        return f"{self.package.title} - {self.item_text}"
    



from django.db import models
from django.contrib.auth.models import User

class GalleryItem(models.Model):
    MEDIA_TYPES = (
        ('image', 'Image'),
        ('video', 'Video'),
    )
    
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='gallery/')
    type = models.CharField(max_length=10, choices=MEDIA_TYPES, default='image')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title or f"{self.type} - {self.id}"
    
    def delete(self, *args, **kwargs):
        storage, path = self.file.storage, self.file.path
        super().delete(*args, **kwargs)
        storage.delete(path)



from ckeditor.fields import RichTextField

class FranchiseInstaller(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17)
    whatsapp_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, null=True)
    location = models.CharField(max_length=300)
    address = models.TextField()
    description = RichTextField(blank=True, null=True, config_name='default')
    map_url = models.URLField(blank=True, null=True, help_text="Google Maps URL for the installer location")
    shop_open_time = models.TimeField()
    shop_close_time = models.TimeField()
    image = models.ImageField(upload_to='installers/profile/', blank=True, null=True)
    banner_image = models.ImageField(upload_to='installers/banner/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'franchise_installers'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.location}"