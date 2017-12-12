from django.conf import settings
import os

def get_image_path(instance, filename):
    return os.path.join("stories", filename)
