# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(LogExternal)
admin.site.register(LogInternal)