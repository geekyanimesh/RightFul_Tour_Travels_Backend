from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PackageViewSet, GalleryImageViewSet, TestimonialViewSet,
    SiteAnnouncementViewSet, SubmitEnquiryView, SubmitContactMessageView
)

router = DefaultRouter()
router.register(r'packages', PackageViewSet)
router.register(r'gallery', GalleryImageViewSet)
router.register(r'testimonials', TestimonialViewSet)
router.register(r'announcements', SiteAnnouncementViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('enquire/', SubmitEnquiryView.as_view(), name='submit-enquiry'),
    path('contact/', SubmitContactMessageView.as_view(), name='submit-contact'),
]