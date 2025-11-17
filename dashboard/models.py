from django.db import models

# Create your models here.


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

class CarWashPackage(models.Model):
    title = models.CharField(max_length=200, default="Essential Care")
    description = models.TextField(
        default="Perfect for maintaining your vehicle's appearance with professional exterior and interior care."
    )
    ideal_for = models.CharField(
        max_length=300, 
        default="Regular maintenance, monthly touch-ups"
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
        return self.title

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