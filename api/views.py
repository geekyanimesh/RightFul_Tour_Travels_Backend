from rest_framework import viewsets, generics
from django.core.mail import EmailMessage
from django.conf import settings
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


# --- Write-Only Endpoints (For Form Submissions with Email Hook) ---

class SubmitEnquiryView(generics.CreateAPIView):
    """Endpoint for the Next.js Package Enquiry form to send POST requests."""
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer

    def perform_create(self, serializer):
        # 1. Save to Neon Database
        instance = serializer.save()
        
        # 2. Construct and Send Email
        subject = f"New Package Enquiry: {instance.package.title}"
        message = (
            f"A new enquiry has been submitted for {instance.package.title}.\n\n"
            f"Client Details:\n"
            f"Name: {instance.name}\n"
            f"Email: {instance.email}\n"
            f"Phone: {instance.phone}\n"
            f"Travel Dates: {instance.travel_dates}\n"
            f"Number of People: {instance.number_of_people}\n"
        )
        
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.ADMIN_NOTIFICATION_EMAILS,
            reply_to=[instance.email]
        )
        email.send(fail_silently=False)

class SubmitContactMessageView(generics.CreateAPIView):
    """Endpoint for the Next.js General Contact form to send POST requests."""
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        # 1. Save to Neon Database
        instance = serializer.save()
        
        # 2. Construct and Send Email
        subject = f"New Contact Request from {instance.name}"
        message = (
            f"A new general contact message has been submitted.\n\n"
            f"Name: {instance.name}\n"
            f"Email: {instance.email}\n"
            f"Phone: {instance.phone}\n"
            f"Message:\n{instance.message}\n"
        )
        
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.ADMIN_NOTIFICATION_EMAILS,
            reply_to=[instance.email]
        )
        email.send(fail_silently=False)