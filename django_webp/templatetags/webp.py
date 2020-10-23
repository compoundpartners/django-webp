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
    converter = WEBPImageConverter()

    if value.__class__.__name__ == 'Image' and hasattr(value, 'file'):
        converter.init(value.file.name, value.file.storage, file_obj=value.file)
    elif value.__class__.__name__ == 'MultiStorageFieldFile':
        converter.init(value.name, value.storage, file_obj=value.file)
    else:
        converter.init(value, staticfiles_storage)

    supports_webp = context.get('supports_webp', False)
    if not supports_webp or WEBP_DEBUG:
        return converter.get_url()

    return converter.get_webp_url()
