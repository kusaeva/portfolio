# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

class HeaderPhoto(models.Model):
    photo = models.ImageField(upload_to='img/header/')
    description = models.CharField(max_length=32)
    is_active = models.BooleanField(default=True)



class Story(models.Model):
    cover = models.CharField(max_length=16)
    name = models.CharField(max_length=16)

class Photo(models.Model):
    name = models.CharField(max_length=16)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
