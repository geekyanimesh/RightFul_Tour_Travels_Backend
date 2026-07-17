from rest_framework import viewsets, generics
from .models import Package, Enquiry, ContactMessage, GalleryImage, Testimonial, SiteAnnouncement
from .serializers import (
    PackageSerializer, EnquirySerializer, ContactMessageSerializer, 
    GalleryImageSerializer, TestimonialSerializer, SiteAnnouncementSerializer
)

# --- Public Read-Only Endpoints ---

class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows Next.js to fetch the list of packages and individual package details."""
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class GalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows Next.js to fetch gallery images."""
    queryset = GalleryImage.objects.all().order_by('-created_at')
    serializer_class = GalleryImageSerializer

class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """Allows Next.js to fetch client reviews."""
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer

class SiteAnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    """Fetches only the active announcements for the Home Page pop-up."""
    queryset = SiteAnnouncement.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = SiteAnnouncementSerializer


# --- Write-Only Endpoints (For Form Submissions) ---

class SubmitEnquiryView(generics.CreateAPIView):
    """Endpoint for the Next.js Package Enquiry form to send POST requests."""
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer

class SubmitContactMessageView(generics.CreateAPIView):
    """Endpoint for the Next.js General Contact form to send POST requests."""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer