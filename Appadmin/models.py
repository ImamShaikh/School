from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Teacher(models.Model):
    name = models.CharField(max_length=255)
    teach_sub = models.CharField(max_length=200)
    expertise = models.CharField(max_length=200)
    image = models.ImageField(upload_to='teachers/', blank=True, null=True)
    p_no = models.CharField(max_length=10)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    experience = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.name}'

class SchoolInfo(models.Model):
    name = models.CharField(max_length=255, default="Govind Ashram Shala Ekshiv")
    logo = models.ImageField(upload_to='school/', blank=True, null=True)
    address = models.TextField(default="Govind Ashram shala Ekshiv, Tal- Malashiras, Dist- Solapur")
    phone = models.CharField(max_length=20, default="+91-9960905064")
    email = models.EmailField(default="info@domain.com")
    office_hours = models.CharField(max_length=255, default="9:00 AM - 5:00 PM")
    vision = models.TextField(default="To nurture young minds with a holistic approach to learning.")
    mission = models.TextField(default="To provide a high-quality education that fosters intellectual, emotional, and social development.")
    history = models.TextField(default="Founded with years of excellence in education...")
    achievements = models.TextField(default="100% passing results, Sports excellence awards...")
    principal_message = models.TextField(default="Dear Parents and Students, Welcome to our school...")
    principal_name = models.CharField(max_length=255, default="Principal Name")
    principal_photo = models.ImageField(upload_to='school/', blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and SchoolInfo.objects.exists():
            return
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "School Information"
        verbose_name_plural = "School Information"

class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    venue = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    registration_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class News(models.Model):
    CATEGORY_CHOICES = [
        ('Admissions', 'Admissions'),
        ('Achievements', 'Achievements'),
        ('Events', 'Events'),
        ('Announcements', 'Announcements'),
        ('General', 'General'),
    ]
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='General')
    summary = models.TextField()
    content = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "News"

class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('Campus', 'Campus'),
        ('Events', 'Events'),
        ('Sports', 'Sports'),
        ('Cultural', 'Cultural'),
        ('Students', 'Students'),
        ('Activities', 'Activities'),
    ]
    image = models.ImageField(upload_to='gallery/')
    title = models.CharField(max_length=255, blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Campus')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title or f"Gallery Image {self.id}"

class ManagementMember(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='management/', blank=True, null=True)
    message = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Facility(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=100, default='fa-school')
    image = models.ImageField(upload_to='facilities/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Facilities"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_no = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Profile of {self.user.username}"

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)
    else:
        # Check if profile exists before saving
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            UserProfile.objects.get_or_create(user=instance)