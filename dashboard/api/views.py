from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from ..models import FranchiseInstaller, HomePage, FranchisePage, PackagesPage, ContactPage, CarWashPackage, GalleryItem
from ..serializers import (
    FranchiseInstallerSerializer,
    HomePageSerializer, 
    FranchisePageSerializer, 
    PackagesPageSerializer, 
    ContactPageSerializer,
    CarWashPackageSerializer,
    GalleryItemSerializer
)

@api_view(['GET'])
def home_data(request):
    """API endpoint for home page data"""
    try:
        home_page = HomePage.objects.first()
        if not home_page:
            return Response(
                {'error': 'Home page data not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = HomePageSerializer(home_page)
        return Response(serializer.data)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def franchise_data(request):
    """API endpoint for franchise page data"""
    try:
        franchise_page = FranchisePage.objects.first()
        if not franchise_page:
            return Response(
                {'error': 'Franchise page data not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = FranchisePageSerializer(franchise_page)
        return Response(serializer.data)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def packages_data(request):
    """API endpoint for packages page data"""
    try:
        packages_page = PackagesPage.objects.first()
        if not packages_page:
            return Response(
                {'error': 'Packages page data not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = PackagesPageSerializer(packages_page)
        return Response(serializer.data)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def contact_data(request):
    """API endpoint for contact page data"""
    try:
        contact_page = ContactPage.objects.first()
        if not contact_page:
            return Response(
                {'error': 'Contact page data not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ContactPageSerializer(contact_page)
        return Response(serializer.data)
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def car_wash_packages(request):
    """API endpoint for all active car wash packages"""
    try:
        packages = CarWashPackage.objects.filter(is_active=True).order_by('created_at')
        serializer = CarWashPackageSerializer(packages, many=True)
        return Response({
            'packages': serializer.data,
            'count': packages.count()
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def package_detail(request, package_id):
    """API endpoint for specific package detail"""
    try:
        package = CarWashPackage.objects.get(id=package_id, is_active=True)
        serializer = CarWashPackageSerializer(package)
        return Response(serializer.data)
    
    except CarWashPackage.DoesNotExist:
        return Response(
            {'error': 'Package not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
def gallery_items(request):
    """API endpoint for gallery items"""
    try:
        items = GalleryItem.objects.all().order_by('-created_at')
        serializer = GalleryItemSerializer(items, many=True)
        return Response({
            'items': serializer.data,
            'count': items.count()
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    

@api_view(['GET'])
def franchise_installers_api(request):
    """API endpoint for franchise installers"""
    try:
        installers = FranchiseInstaller.objects.filter(is_active=True).order_by('-created_at')
        serializer = FranchiseInstallerSerializer(installers, many=True)
        return Response({
            'installers': serializer.data,
            'count': installers.count()
        })
    
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )    