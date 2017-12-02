# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class HeaderPhoto(models.Model):
    photo = models.ImageField(upload_to='img/header/')
    description = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)
