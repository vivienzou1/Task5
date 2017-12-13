from django.db import models
from registration.models import TimeStampedModel
from django.contrib.auth.models import User
# Create your models here.


class Chat(TimeStampedModel):
    from_whom = models.ForeignKey(User, related_name="from_whom", blank=False, null=False)
    to_whom = models.ForeignKey(User, related_name="to_whom", blank=False, null=False)
    content = models.CharField(max_length=600)