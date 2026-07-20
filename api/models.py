from django.db import models
from cloudinary.models import CloudinaryField

class Package(models.Model):
    """Stores the Tour Packages details."""
    objects = models.Manager()

    title = models.CharField(max_length=200)
    itinerary = models.TextField()
    inclusions = models.TextField()
    exclusions = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image')

    def __str__(self):
        return str(self.title)


class Enquiry(models.Model):
    """Captures leads specific to a tour package."""
    objects = models.Manager()

    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='enquiries')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    travel_dates = models.CharField(max_length=100)
    number_of_people = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254, default="client@example.com")

    def __str__(self):
        return f"{self.name} - {self.package.title}"


class ContactMessage(models.Model):
    """Captures general contact form submissions."""
    objects = models.Manager()

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(max_length=254, default="client@example.com")

    def __str__(self):
        return f"{self.name} - {self.phone}"


class GalleryImage(models.Model):
    """Stores the photo collection for the Gallery page."""
    objects = models.Manager()

    image = CloudinaryField('image')
    caption = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.caption) or "Gallery Image"


class Testimonial(models.Model):
    """Stores past client reviews."""
    objects = models.Manager()

    name = models.CharField(max_length=100)
    review_text = models.TextField()
    photo = CloudinaryField('image', blank=True, null=True)
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


class SiteAnnouncement(models.Model):
    """Manages the content for the Home Page promotional pop-ups."""
    objects = models.Manager()

    title = models.CharField(max_length=200)
    content = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)


class CustomQuote(models.Model):
    """Captures custom quote requests."""
    objects = models.Manager()

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    service_type = models.CharField(max_length=100)
    destination = models.CharField(max_length=200, blank=True)
    travel_date = models.CharField(max_length=100, blank=True)
    duration = models.CharField(max_length=50, blank=True)
    adults = models.CharField(max_length=10, default="2")
    children = models.CharField(max_length=10, default="0")
    budget = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service_type}"