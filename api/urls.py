from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PackageViewSet, GalleryImageViewSet, TestimonialViewSet,
    SiteAnnouncementViewSet, SubmitEnquiryView, SubmitContactMessageView, SubmitCustomQuoteView,
    create_order, verify_payment
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
    path('quote/', SubmitCustomQuoteView.as_view(), name='submit-quote'),
    
    # Razorpay Endpoints
    path('razorpay/create-order/', create_order, name='create_order'),
    path('razorpay/verify/', verify_payment, name='verify_payment'),
]