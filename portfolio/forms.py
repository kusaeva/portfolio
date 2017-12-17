import string
import zipfile
try:
    from zipfile import BadZipFile
except ImportError:
    # Python 2.
    from zipfile import BadZipfile as BadZipFile
import logging
import os
from io import BytesIO

try:
    import Image
except ImportError:
    from PIL import Image


from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.encoding import force_text
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile

from photologue.models import Gallery, Photo
from photologue.forms import UploadZipForm as UploadZipFormDefault
from .models import Lovestory, Family, Travel, Portrait

logger = logging.getLogger('photologue.forms')


class UploadZipForm(UploadZipFormDefault):
    caption = ''
    description = ''
    GALLERY = _('GALLERY')
    LOVESTORY = _('LOVESTORY')
    FAMILY = _('FAMILY')
    PORTRAIT = _('PORTRAIT')
    TRAVEL = _('TRAVEL')
    GALLERY_TYPE_CHOICES = (
        (GALLERY, _('Wedding')),
        (LOVESTORY, _('Lovestory')),
        (FAMILY, _('Family')),
        (PORTRAIT, _('Portrait')),
        (TRAVEL, _('Travel')),
    )

    gallery_type = forms.ChoiceField(
        choices=GALLERY_TYPE_CHOICES,
    )

    def save(self, request=None, zip_file=None):
        print(self.cleaned_data['gallery_type'])

        if not zip_file:
            zip_file = self.cleaned_data['zip_file']
            encoded = zip_file._name.encode('utf-8').decode()
            zipname = encoded.split('.')[0]
            zip = zipfile.ZipFile(zip_file)
            count = 1
            current_site = Site.objects.get(id=settings.SITE_ID)
        if self.cleaned_data['gallery']:
            logger.debug('Using pre-existing gallery.')
            gallery = self.cleaned_data['gallery']
        else:
            logger.debug(
                force_text('Creating new gallery "{0}".')
                .format(self.cleaned_data['title']))
            gallery_type_cls = {
                'GALLERY': Gallery,
                'LOVESTORY': Lovestory,
                'FAMILY': Family,
                'PORTRAIT': Portrait,
                'TRAVEL': Travel,
            }
            gallery = gallery_type_cls[self.cleaned_data['gallery_type']].objects.create(
                title=self.cleaned_data['title'],
                slug=slugify(self.cleaned_data['title']),
                description=self.cleaned_data['description'],
                is_public=self.cleaned_data['is_public'])
            gallery.sites.add(current_site)

        for filename in sorted(zip.namelist()):
            logger.debug('Reading file "{0}".'.format(filename))

            if filename.startswith('__') or filename.startswith('.'):
                logger.debug('Ignoring file "{0}".'.format(filename))
                continue

            if os.path.dirname(filename):
                logger.warning('Ignoring file "{0}" as it is in a subfolder;\
                               all images should be in the top '
                               'folder of the zip.'.format(filename))
                if request:
                    messages.warning(request,
                                     _('Ignoring file "{filename}"\
                                       as it is in a subfolder;\
                                       all images should \
                                       be in the top folder of the zip.')
                                     .format(filename=filename),
                                     fail_silently=True)
                continue

            data = zip.read(filename)

            if not len(data):
                logger.debug('File "{0}" is empty.'.format(filename))
                continue

            photo_title_root = self.cleaned_data['title'] if self.cleaned_data['title'] else gallery.title

            # A photo might already exist with the same slug. So it's somewhat inefficient,
            # but we loop until we find a slug that's available.
            while True:
                photo_title = ' '.join([photo_title_root, str(count)])
                slug = slugify(photo_title)
                if Photo.objects.filter(slug=slug).exists():
                    count += 1
                    continue
                break

            photo = Photo(title=photo_title,
                          slug=slug,
                          caption=self.cleaned_data['caption'],
                          is_public=self.cleaned_data['is_public'])

            # Basic check that we have a valid image.
            try:
                file = BytesIO(data)
                opened = Image.open(file)
                opened.verify()
            except Exception:
                # Pillow (or PIL) doesn't recognize it as an image.
                # If a "bad" file is found we just skip it.
                # But we do flag this both in the logs and to the user.
                logger.error('Could not process file "{0}" in the .zip archive.'.format(
                    filename))
                if request:
                    messages.warning(request,
                                     _('Could not process file "{0}" in the .zip archive.').format(
                                         filename),
                                     fail_silently=True)
                continue

            contentfile = ContentFile(data)
            photo.image.save("%s/%s" % (zipname, filename), contentfile)
            photo.save()
            photo.sites.add(current_site)
            gallery.photos.add(photo)
            count += 1

        zip.close()

        if request:
            messages.success(request,
                             _('The photos have been added to gallery "{0}".')
                             .format(
                                 gallery.title),
                             fail_silently=True)
