# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import HeaderPhoto, Story, Photo


admin.site.register(HeaderPhoto)
admin.site.register(Story)
admin.site.register(Photo)
