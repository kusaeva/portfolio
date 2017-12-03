# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import HeaderPhoto


def index(request):
    header_photos = HeaderPhoto.objects.filter(is_active=True)
    header_photo = header_photos[0] if header_photos else None
    context = {'header_photo': header_photo}
    return render(request, 'portfolio/index.html', context)
