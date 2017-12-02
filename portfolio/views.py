# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import HeaderPhoto


def index(request):
    header_photo = HeaderPhoto.objects.filter(is_active=True)[0]
    context = {'header_photo': header_photo}
    return render(request, 'portfolio/index.html', context)
