# -*- coding: utf-8 -*-
import os
import logging

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage

from django_webp.utils import WEBPImageConverter, WEBP_DEBUG


register = template.Library()

@register.simple_tag(takes_context=True)
def webp(context, value):
    if value:
        converter = WEBPImageConverter()
        class_name = value.__class__.__name__

        try:
            file_obj = value.file
        except:
            file_obj = None

        if class_name == 'Image' and hasattr(value, 'file'):
            converter.init(value.file.name, value.file.storage, file_obj=file_obj)
        elif class_name == 'MultiStorageFieldFile':
            converter.init(value.name, value.storage, file_obj=file_obj)
        elif class_name == 'ThumbnailFile':
            converter.init(value.name, value.storage, file_obj=file_obj)
        else:
            converter.init(value, staticfiles_storage)

        supports_webp = context.get('supports_webp', False)
        if not supports_webp or WEBP_DEBUG:
            return converter.get_url()
        return converter.get_webp_url()

    return ''
