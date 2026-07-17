from django.contrib import admin
from .models import Package, Enquiry, ContactMessage, GalleryImage, Testimonial, SiteAnnouncement

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')  # type: ignore
    search_fields = ('title',)

@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    # Shows these specific columns in the admin table
    list_display = ('name', 'phone', 'package', 'travel_dates', 'created_at')  # type: ignore
    # Adds a sidebar filter so the client can sort leads by package or date
    list_filter = ('package', 'created_at')
    search_fields = ('name', 'phone')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')  # type: ignore
    list_filter = ('created_at',)
    search_fields = ('name', 'phone', 'message')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'created_at')  # type: ignore
    search_fields = ('caption',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'rating', 'created_at')  # type: ignore
    list_filter = ('rating', 'created_at')
    search_fields = ('name', 'review_text')

@admin.register(SiteAnnouncement)
class SiteAnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')  # type: ignore
    # Allows the client to quickly toggle the pop-up on or off from the list view
    list_editable = ('is_active',)
    list_filter = ('is_active',)