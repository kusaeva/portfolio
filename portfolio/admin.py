# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.contrib import admin
from django.utils.translation import ungettext, ugettext_lazy as _
from django.shortcuts import render
from django.contrib.admin import helpers
from django.http import HttpResponseRedirect

from photologue.admin import PhotoEffect, Watermark
from photologue.admin import PhotoAdmin as PhotoAdminDefault
from photologue.admin import GalleryAdmin as GalleryAdminDefault

from .forms import UploadZipForm
from photologue.models import Gallery, Photo
from .models import Lovestory, Family, Portrait, Travel


class PhotoAdminForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = ('sites', 'caption', 'description',)


class GalleryAdminForm(forms.ModelForm):
    class Meta:
        model = Gallery
        exclude = ('sites', 'description', 'date_added',)


class GalleryAdmin(GalleryAdminDefault):
    form = GalleryAdminForm


class LovestoryAdminForm(forms.ModelForm):
    class Meta:
        model = Lovestory
        exclude = ('sites', 'description', 'date_added',)


class LovestoryAdmin(GalleryAdminDefault):
    form = LovestoryAdminForm


class FamilyAdminForm(forms.ModelForm):
    class Meta:
        model = Family
        exclude = ('sites', 'description', 'date_added',)


class FamilyAdmin(GalleryAdminDefault):
    form = FamilyAdminForm


class TravelAdminForm(forms.ModelForm):
    class Meta:
        model = Travel
        exclude = ('sites', 'description', 'date_added',)


class TravelAdmin(GalleryAdminDefault):
    form = TravelAdminForm


class PortraitAdminForm(forms.ModelForm):
    class Meta:
        model = Portrait
        exclude = ('sites', 'description', 'date_added',)


class PortraitAdmin(GalleryAdminDefault):
    form = PortraitAdminForm


class PhotoAdmin(PhotoAdminDefault):
    form = PhotoAdminForm

    def upload_zip(self, request):
        context = {
            'title': _('Upload a zip archive of photos'),
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        # Handle form requesta
        if request.method == 'POST':
            form = UploadZipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('..')
        else:
            form = UploadZipForm()
        context['form'] = form
        context['adminform'] = helpers.AdminForm(
            form,
            list([(None, {'fields': form.base_fields})]),
            {})
        return render(
            request,
            'admin/photologue/photo/upload_zip.html',
            context)


admin.site.unregister(Photo)
admin.site.unregister(Gallery)
admin.site.unregister(PhotoEffect)
admin.site.unregister(Watermark)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Lovestory, GalleryAdmin)
admin.site.register(Family, GalleryAdmin)
admin.site.register(Travel, GalleryAdmin)
admin.site.register(Portrait, GalleryAdmin)
