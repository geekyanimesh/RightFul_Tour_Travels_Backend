from rest_framework import viewsets, generics
from django.core.mail import EmailMessage
from django.conf import settings
from .models import Package, Enquiry, ContactMessage, GalleryImage, Testimonial, SiteAnnouncement, CustomQuote
from .serializers import (
    PackageSerializer, EnquirySerializer, ContactMessageSerializer, 
    GalleryImageSerializer, TestimonialSerializer, SiteAnnouncementSerializer, CustomQuoteSerializer
)

class PackageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

class GalleryImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GalleryImage.objects.all().order_by('-created_at')
    serializer_class = GalleryImageSerializer

class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Testimonial.objects.all().order_by('-created_at')
    serializer_class = TestimonialSerializer

class SiteAnnouncementViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteAnnouncement.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = SiteAnnouncementSerializer

class SubmitEnquiryView(generics.CreateAPIView):
    queryset = Enquiry.objects.all()
    serializer_class = EnquirySerializer

    def perform_create(self, serializer):
        instance = serializer.save()
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
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
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

class SubmitCustomQuoteView(generics.CreateAPIView):
    queryset = CustomQuote.objects.all()
    serializer_class = CustomQuoteSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        subject = f"New Custom Quote Request: {instance.service_type} from {instance.name}"
        message = (
            f"A new custom quote request has been submitted.\n\n"
            f"Client Details:\n"
            f"Name: {instance.name}\n"
            f"Email: {instance.email}\n"
            f"Phone: {instance.phone}\n\n"
            f"Trip / Event Details:\n"
            f"Service Type: {instance.service_type}\n"
            f"Destination: {instance.destination}\n"
            f"Tentative Date: {instance.travel_date}\n"
            f"Duration: {instance.duration} Days\n"
            f"Adults: {instance.adults} | Children: {instance.children}\n"
            f"Estimated Budget: {instance.budget}\n\n"
            f"Additional Requirements:\n{instance.message}\n"
        )
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=settings.ADMIN_NOTIFICATION_EMAILS,
            reply_to=[instance.email]
        )
        email.send(fail_silently=False)