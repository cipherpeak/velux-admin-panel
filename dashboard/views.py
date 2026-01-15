from .models import CarWashPackage, HomePage, FranchisePage, PackageInclude, PackagesPage, ContactPage
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import GalleryItem
from .forms import GalleryItemForm
from django.contrib import messages

def create_default_cards():
    """Create default card objects if they don't exist"""
    if not HomePage.objects.exists():
        HomePage.objects.create(
            title="Welcome to Our Home",
            description="Discover amazing experiences and services we offer to make your journey unforgettable.",
            image="default_images/home-default.jpg"
        )
    
    if not FranchisePage.objects.exists():
        FranchisePage.objects.create(
            title="Franchise Opportunities",
            description="Join our growing network of franchises and be part of our success story.",
            image="default_images/franchise-default.jpg"
        )
    
    if not PackagesPage.objects.exists():
        PackagesPage.objects.create(
            title="Our Packages",
            description="Explore our carefully crafted packages designed to meet your every need.",
            image="default_images/packages-default.jpg"
        )
    
    if not ContactPage.objects.exists():
        ContactPage.objects.create(
            title="Get In Touch",
            description="Contact us for any inquiries or support. We're here to help you.",
            image="default_images/contact-default.jpg"
        )

@login_required
def dashboard(request):
    create_default_cards()
    
    context = {
        'home_card': HomePage.objects.first(),
        'franchise_card': FranchisePage.objects.first(),
        'packages_card': PackagesPage.objects.first(),
        'contact_card': ContactPage.objects.first(),
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def update_card(request):
    """Update card data via form submission"""
    if request.method == 'POST':
        try:
            card_id = request.POST.get('card_id')
            title = request.POST.get('title')
            description = request.POST.get('description')
            media_type = request.POST.get('media_type')
            media_file = request.FILES.get('media_file')
            
            print(f"Card ID received: '{card_id}' (type: {type(card_id)})")
            
            # Create default cards first to ensure they exist
            create_default_cards()
            
            # Determine which model to update based on card_id
            if card_id == '1':  # Home Page
                card = HomePage.objects.first()
            elif card_id == '2':  # Franchise Page
                card = FranchisePage.objects.first()
            elif card_id == '3':  # Packages Page
                card = PackagesPage.objects.first()
            elif card_id == '4':  # Contact Page
                card = ContactPage.objects.first()
            else:
                messages.error(request, f'Invalid card ID: {card_id}')
                return redirect('dashboard:dashboard')
            
            if not card:
                messages.error(request, 'Card not found')
                return redirect('dashboard:dashboard')
            
            # Update fields
            card.title = title
            card.description = description
            card.media_type = media_type
            
            # Handle media file update if provided
            if media_file:
                if media_type == 'video':
                    # Delete old video if exists
                    if card.video and not card.video.name.startswith('default_images/'):
                        card.video.delete(save=False)
                    # Save new video
                    card.video = media_file
                    # Keep image as fallback
                    if not card.image or card.image.name.startswith('default_images/'):
                        # Set a default image if none exists
                        card.image = 'default_images/default-video-thumbnail.jpg'
                else:  # image
                    # Delete old image if it's not the default
                    if card.image and not card.image.name.startswith('default_images/'):
                        card.image.delete(save=False)
                    # Save new image
                    card.image = media_file
            
            card.save()
            messages.success(request, 'Card updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating card: {str(e)}')
    
    return redirect('dashboard:dashboard')





@login_required
def package_page(request):
    # Get all active packages
    packages = CarWashPackage.objects.filter(is_active=True).order_by('created_at')
    
    context = {
        'packages': packages,
    }
    return render(request, 'dashboard/package_plans.html', context)

def create_package(request):
    if request.method == 'POST':
        try:
            # Create new package
            package = CarWashPackage.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                ideal_for=request.POST.get('ideal_for'),
                button_text=request.POST.get('button_text'),
                is_active=True
            )
            
            # Get includes from form
            includes_list = request.POST.getlist('includes')
            
            # Create includes
            for index, include_text in enumerate(includes_list):
                if include_text.strip():
                    PackageInclude.objects.create(
                        package=package,
                        item_text=include_text.strip(),
                        order=index
                    )
            
            messages.success(request, 'Package created successfully!')
            
        except Exception as e:
            messages.error(request, f'Error creating package: {str(e)}')
    
    return redirect('dashboard:packages')

@login_required
def update_package(request, package_id):
    if request.method == 'POST':
        package = get_object_or_404(CarWashPackage, id=package_id)
        
        try:
            # Update package fields
            package.title = request.POST.get('title')
            package.description = request.POST.get('description')
            package.ideal_for = request.POST.get('ideal_for')
            package.button_text = request.POST.get('button_text')
            package.save()
            
            # Get includes from form
            includes_list = request.POST.getlist('includes')
            
            # Clear existing includes
            PackageInclude.objects.filter(package=package).delete()
            
            # Create new includes
            for index, include_text in enumerate(includes_list):
                if include_text.strip():
                    PackageInclude.objects.create(
                        package=package,
                        item_text=include_text.strip(),
                        order=index
                    )
            
            messages.success(request, 'Package updated successfully!')
            
        except Exception as e:
            messages.error(request, f'Error updating package: {str(e)}')
    
    return redirect('dashboard:packages')






@login_required
def gallery_view(request):
    """Display all gallery items in masonry layout"""
    gallery_items = GalleryItem.objects.filter(created_by=request.user)
    
    context = {
        'gallery_items': gallery_items,
        'active_page': 'gallery'
    }
    return render(request, 'dashboard/gallery.html', context)

@login_required
def add_gallery_item(request):
    """Handle both image and video uploads"""
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.created_by = request.user
            
            # Determine file type based on MIME type
            file = request.FILES.get('file')
            if file:
                if file.content_type.startswith('image/'):
                    gallery_item.type = 'image'
                elif file.content_type.startswith('video/'):
                    gallery_item.type = 'video'
            
            gallery_item.save()
            
            messages.success(request, f'{gallery_item.type.title()} uploaded successfully!')
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': f'{gallery_item.type.title()} uploaded successfully!'
                })
            return redirect('dashboard:gallery')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
            messages.error(request, 'There was an error uploading your file. Please check the form.')
    else:
        form = GalleryItemForm()
    
    context = {
        'form': form,
        'active_page': 'gallery'
    }
    return render(request, 'dashboard/gallery.html', context)

@login_required
def add_image(request):
    """Specific view for image uploads"""
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.created_by = request.user
            gallery_item.type = 'image'
            gallery_item.save()
            
            messages.success(request, 'Image uploaded successfully!')
            return redirect('dashboard:gallery')
        else:
            messages.error(request, 'There was an error uploading your image. Please check the form.')
    
    return redirect('dashboard:gallery')

@login_required
def add_video(request):
    """Specific view for video uploads"""
    if request.method == 'POST':
        form = GalleryItemForm(request.POST, request.FILES)
        
        if form.is_valid():
            gallery_item = form.save(commit=False)
            gallery_item.created_by = request.user
            gallery_item.type = 'video'
            gallery_item.save()
            
            messages.success(request, 'Video uploaded successfully!')
            return redirect('dashboard:gallery')
        else:
            messages.error(request, 'There was an error uploading your video. Please check the form.')
    
    return redirect('dashboard:gallery')

@login_required
@require_POST
def delete_gallery_item(request, item_id):
    """Delete a gallery item"""
    gallery_item = get_object_or_404(GalleryItem, id=item_id, created_by=request.user)
    
    item_type = gallery_item.type
    gallery_item.delete()
    
    messages.success(request, f'{item_type.title()} deleted successfully!')
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{item_type.title()} deleted successfully!'
        })
    
    return redirect('dashboard:gallery')

@login_required
def get_gallery_items(request):
    """API endpoint to get gallery items (for AJAX requests)"""
    gallery_items = GalleryItem.objects.filter(created_by=request.user)
    
    items_data = []
    for item in gallery_items:
        items_data.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'file_url': item.file.url,
            'type': item.type,
            'created_at': item.created_at.strftime('%Y-%m-%d %H:%M'),
        })
    
    return JsonResponse({
        'items': items_data
    })





from django.views.decorators.http import require_POST
from .models import FranchiseInstaller
from .forms import FranchiseInstallerForm

@login_required
def franchise_installers(request):
    """Display all franchise installers"""
    installers = FranchiseInstaller.objects.filter(is_active=True).order_by('-created_at')
    form = FranchiseInstallerForm()  # Create empty form for the create modal
    
    context = {
        'installers': installers,
        'form': form,
        'active_page': 'franchise_installers'
    }
    return render(request, 'dashboard/franchise_installers.html', context)

@login_required
def create_installer(request):
    """Create new franchise installer"""
    if request.method == 'POST':
        form = FranchiseInstallerForm(request.POST, request.FILES)
        print(form,"this is form")
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Installer created successfully!')
                return redirect('dashboard:franchise_installers')
            except Exception as e:
                messages.error(request, f'Error creating installer: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    # If GET request or form invalid, show the page with form in modal
    return redirect('dashboard:franchise_installers')

@login_required
def edit_installer(request, installer_id):
    """Edit franchise installer"""
    installer = get_object_or_404(FranchiseInstaller, id=installer_id)
    
    if request.method == 'POST':
        form = FranchiseInstallerForm(request.POST, request.FILES, instance=installer)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Installer updated successfully!')
                return redirect('dashboard:franchise_installers')
            except Exception as e:
                messages.error(request, f'Error updating installer: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    # If GET request, show the edit modal with current data
    installers = FranchiseInstaller.objects.filter(is_active=True).order_by('-created_at')
    context = {
        'installers': installers,
        'editing_installer': installer,
        'active_page': 'franchise_installers'
    }
    return render(request, 'dashboard/franchise_installers.html', context)

@login_required
def delete_installer(request, installer_id):
    """Delete franchise installer (soft delete)"""
    installer = get_object_or_404(FranchiseInstaller, id=installer_id)
    
    try:
        installer.is_active = False
        installer.save()
        messages.success(request, 'Installer deleted successfully!')
    except Exception as e:
        messages.error(request, f'Error deleting installer: {str(e)}')
    
    return redirect('dashboard:franchise_installers')