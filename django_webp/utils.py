import os
import logging
from PIL import Image

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static

WEBP_DEBUG = getattr(settings, 'WEBP_DEBUG', settings.DEBUG)

class WEBPImageConverter:

    def init(self, name, storage, file_obj=None, image=None, new_name=None):
        try:
            self.name = name
            self.storage = storage
            self.file_obj = file_obj
            self.image = image
            self.new_name = new_name
            self.path = self.storage_path(self.name)
            if not self.new_name:
                self.new_name = '.'.join([*self.name.split('.')[:-1], 'webp'])
        except:
            logger = logging.getLogger(__name__)
            logger.warn('WEBP image init error, source name is %s' % name)

    def storage_path(self, name):
        if 'S3' in self.storage.__class__.__name__:
            return name
        return  self.storage.path(name)

    def get_url(self):
        if not self.storage.exists(self.path):
            return ''
        return self.storage.url(self.name)

    def get_webp_url(self):
        new_path = self.storage_path(self.new_name)

        if not self.storage.exists(self.path):
            return ''

        if not self.generate_webp_image(new_path):
            return self.get_url()

        return self.storage.url(self.new_name)

    def generate_webp_image(self, generated_path):
        if self.storage.exists(generated_path):
            return True

        if not self.image:
            try:
                self.image = Image.open(self.file_obj or self.path)
            except:
                return False

        try:
            storage_file = self.storage.open(generated_path, "wb")
            self.image.save(storage_file, 'WEBP')
            storage_file.close()
            return True
        except KeyError:
            logger = logging.getLogger(__name__)
            logger.warn('WEBP is not installed in pillow')
        except (IOError, OSError):
            logger = logging.getLogger(__name__)
            logger.warn('WEBP image could not be saved in %s' % generated_path)

        return False



def store_as_webp(sender, **kwargs):
    converter = WEBPImageConverter()
    converter.init(sender.name, sender.storage, image=sender.image)
    converter.get_webp_url()
    #webp_path = sender.storage.path('.'.join([sender.name, 'webp']))
    #sender.image.save(webp_path, 'webp')
