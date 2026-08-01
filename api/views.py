import razorpay
from razorpay.errors import SignatureVerificationError

from django.conf import settings
from rest_framework import viewsets, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import EmailMessage
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

# Razorpay Integration
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@api_view(['POST'])
def create_order(request):
    try:
        amount = int(request.data.get('amount', 0)) * 100 
        currency = "INR"
        
        razorpay_order = client.order.create({  # type: ignore
            "amount": amount,
            "currency": currency,
            "payment_capture": "1"
        })
        
        return Response({
            'order_id': razorpay_order['id'],
            'amount': amount,
            'currency': currency,
            'key': settings.RAZORPAY_KEY_ID
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def verify_payment(request):
    try:
        payment_id = request.data.get('razorpay_payment_id')
        order_id = request.data.get('razorpay_order_id')
        signature = request.data.get('razorpay_signature')
        
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        
        client.utility.verify_payment_signature(params_dict)  # type: ignore
        return Response({'status': 'Payment Verified'}, status=status.HTTP_200_OK)
    except SignatureVerificationError:
        return Response({'error': 'Invalid Signature'}, status=status.HTTP_400_BAD_REQUEST)