# -*- coding: utf-8 -*-
import mimetypes
import os
import logging

from django import template
from django.conf import settings
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.safestring import mark_safe

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


def convert(value):
    webp_value = None
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

        value = converter.get_url() or value.url
        webp_value = converter.get_webp_url()
    return value, webp_value


@register.simple_tag
def webp_picture(value, **kwargs):
    kwargs_text = ' '.join([''] + [f'{key}="{value}"' for key, value in kwargs.items()])

    value, webp_value = convert(value)

    if webp_value:
        return mark_safe(f'<picture><source srcset="{webp_value}" type="image/webp"/><img src="{value}"{kwargs_text}/></picture>')
    else:
        return mark_safe(f'<img src="{value}"{kwargs_text}/>')


@register.simple_tag
def webp_imageset(value):
    value, webp_value = convert(value)
    mimetype = mimetypes.guess_type(value)[0]

    if webp_value:
        return f'image-set(url({webp_value}) type(image/webp), url({value}) type({mimetype})'
    else:
        return f'url({value})'
