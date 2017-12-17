# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from photologue.models import Gallery
from .models import Lovestory, Portrait, Family, Travel


def index(request):
    def get_cover(gallery):
        cover = None
        for photo in gallery.photos.all():
            if photo.is_cover:
                return photo
        if not cover:
            return gallery.photos.all()[0]

    def get_weddings():
        objects = Gallery.objects.on_site().is_public()
        return [{'slug': obj.title, 'cover':get_cover(obj).get_display_url} for obj in objects]

    def get_lovestories():
        objects = Lovestory.objects.all()
        return [{'slug': obj.title, 'cover':get_cover(obj).get_display_url} for obj in objects]

    def get_families():
        objects = Family.objects.all()
        return [{'slug': obj.title, 'cover':get_cover(obj).get_display_url} for obj in objects]

    def get_travel():
        objects = Travel.objects.all()
        return [{'slug': obj.title, 'cover':get_cover(obj).get_display_url} for obj in objects]

    def get_portraits():
        objects = Portrait.objects.all()
        return [{'slug': obj.title, 'cover':get_cover(obj).get_display_url} for obj in objects]




    weddings = get_weddings()
    lovestories = get_lovestories()
    families = get_families()
    travel = get_travel()
    portraits = get_portraits()
    context = { 'weddings': weddings,
		'lovestories': lovestories,
		'families': families,
		'travel': travel,
		'portarits': portraits
		}
    return render(request, 'portfolio/index.html', context)
