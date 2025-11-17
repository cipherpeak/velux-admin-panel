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