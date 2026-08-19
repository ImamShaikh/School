from django.db import models

class contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone_no = models.CharField(max_length=10)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} sent a message'

class registration(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    stud_name = models.CharField(max_length=300)
    M_name = models.CharField(max_length=300)
    DOB = models.CharField(max_length=120)
    gender= models.CharField(max_length=50)
    religion = models.CharField(max_length=90)
    category = models.CharField(max_length=30)
    P_O_B = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    M_no = models.CharField(max_length=10)
    P_adhar = models.CharField(max_length=12)
    C_adhar = models.CharField(max_length=12)
    street = models.CharField(max_length=150)
    landmark =models.CharField(max_length=140)
    state = models.CharField(max_length=150)
    pin_code = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.stud_name} (Status: {self.status})'