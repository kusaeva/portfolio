# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Wedding, Lovestory, Portrait, Family, Travel


def index(request):
    def get_cover(gallery):
        cover = None
        for photo in gallery.photos.all():
            if photo.is_cover:
                return photo
        if not cover:
            return gallery.photos.all()[0]

    def get_objects(cls_name):
        objects = cls_name.objects.all()
        return [{'slug': obj.title, 'cover': get_cover(obj).get_display_url} for obj in objects]

    context = {'weddings': get_objects(Wedding),
               'lovestories': get_objects(Lovestory),
               'families': get_objects(Family),
               'travel': get_objects(Travel),
               'portraits': get_objects(Portrait)
               }
    return render(request, 'portfolio/index.html', context)
