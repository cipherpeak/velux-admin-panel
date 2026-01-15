from django import forms
from .models import GalleryItem

class GalleryItemForm(forms.ModelForm):
    class Meta:
        model = GalleryItem
        fields = ['title', 'description', 'file', 'type']
        widgets = {
            'type': forms.HiddenInput(),
        }
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError("Please select a file to upload.")
        
        file_type = self.cleaned_data.get('type')
        
        if file_type == 'image':
            # Validate image file
            valid_image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
            valid_image_mimes = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']
            
            if not any(file.name.lower().endswith(ext) for ext in valid_image_extensions):
                raise forms.ValidationError("Unsupported image format. Please upload JPG, PNG, GIF, BMP, or WebP files.")
            
            if file.content_type not in valid_image_mimes:
                raise forms.ValidationError("Invalid image file type.")
            
            # Check file size (10MB limit for images)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("Image file size must be less than 10MB.")
        
        elif file_type == 'video':
            # Validate video file
            valid_video_extensions = ['.mp4', '.webm', '.mov', '.avi']
            valid_video_mimes = ['video/mp4', 'video/webm', 'video/quicktime', 'video/x-msvideo']
            
            if not any(file.name.lower().endswith(ext) for ext in valid_video_extensions):
                raise forms.ValidationError("Unsupported video format. Please upload MP4, WebM, MOV, or AVI files.")
            
            if file.content_type not in valid_video_mimes:
                raise forms.ValidationError("Invalid video file type.")
            
            # Check file size (50MB limit for videos)
            if file.size > 50 * 1024 * 1024:
                raise forms.ValidationError("Video file size must be less than 50MB.")
        
        return file
    



from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import FranchiseInstaller

class FranchiseInstallerForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)
    
    class Meta:
        model = FranchiseInstaller
        fields = [
            'name', 'email', 'phone_number', 'whatsapp_number', 'location', 'address',
            'description', 'map_url', 'shop_open_time', 'shop_close_time', 
            'image', 'banner_image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter installer name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter WhatsApp number (optional)'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full address',
                'rows': 3
            }),
            'map_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Google Maps URL'
            }),
            'shop_open_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'shop_close_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'banner_image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }