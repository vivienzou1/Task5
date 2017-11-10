from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    last_name = models.CharField(max_length=20, blank=False)
    first_name = models.CharField(max_length=20, blank=False)
    middle_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=32, blank=False)
    address = models.CharField(max_length=150, blank=False)
    date_of_birth = models.DateField(blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False)
    ssn = models.CharField(max_length=9, min_length=9, blank=False)
    USER_CHOICES = (
        ('C', 'client'),
        ('E', 'employee'),
    )
    type = models.CharField(max_length=1, choices=USER_CHOICES, blank=False)


    def __unicode__(self):
        return 'Profile(id=' + str(self.id) + ')'
