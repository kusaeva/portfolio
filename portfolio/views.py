# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import HeaderPhoto, Story, Photo



def index(request):
    header_photos = HeaderPhoto.objects.filter(is_active=True)
    header_photo = header_photos[0] if header_photos else None
    story = Story(name='manko', cover='13.jpg',)
    story.save()
    story2 = Story(name='postoyalko', cover='009.jpg',)
    story2.save()
    story3 = Story(name='nazarkevich', cover='544.jpg',)
    story3.save()
    story4 = Story(name='manko', cover='191.jpg',)
    story4.save()
    story5 = Story(name='postoyalko', cover='264.jpg',)
    story5.save()
    story6 = Story(name='nazarkevich', cover='098.jpg',)
    story6.save()
    story.photo_set.create(name='037.jpg',)
    story.save()
    weddings = [ story, story2, story3, story4]
    lovestories = [ story5, story6, story, story2 ]
    galleries = Gallery.objects.all()

    weddings = [{'slug': gallery.title, 'cover':gallery.photos.all()[0].get_display_url} for gallery in galleries ]
    lovestories = weddings
    context = {'header_photo': header_photo, 'weddings': weddings, 'lovestories': lovestories}
    return render(request, 'portfolio/index.html', context)


from photologue.models import Gallery
def gallery(request):
    galleries = Gallery.objects.all()

    gallery = galleries.get(title="Postoyalko")
    # photos = [photo.get_display_url() for photo in gallery.photos.all()]
    # for p in photos:
    #     print(p)
    context = { 'photos': ['010.jpg',
        '022.jpg',
        '028.jpg',
        '054.jpg',
        '066.jpg',
        '073.jpg',
        '081.jpg',
        '098.jpg',
        '113.jpg',
        '116.jpg',
        '133.jpg',
        '163.jpg',
        '169.jpg',
        '182.jpg',
        '187.jpg',
        '213.jpg',
        '231.jpg',
        '253.jpg',
        '258.jpg',
        '262.jpg',
        '263.jpg',
        '335.jpg',
        '385.jpg',
        '410.jpg',
        '418.jpg',
        '482.jpg',
        '483.jpg',
        '529.jpg',
        '544.jpg',
        '564.jpg',
        '605.jpg',
        '606.jpg',
        '607.jpg',
        '617.jpg',
        '652.jpg',
        '715.jpg',
        '742.jpg',
        '750.jpg',
        '755.jpg']}
    return render(request, 'portfolio/gallery.html', context)
