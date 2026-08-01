# serializers.py

from rest_framework import serializers
from .models import Package, Enquiry, ContactMessage, GalleryImage, Testimonial, SiteAnnouncement, CustomQuote

class PackageSerializer(serializers.ModelSerializer):
    is_active_flash_sale = serializers.ReadOnlyField()

    class Meta:
        model = Package
        fields = '__all__'

class EnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class SiteAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteAnnouncement
        fields = '__all__'

class CustomQuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomQuote
        fields = '__all__'