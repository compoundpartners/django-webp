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
def webp(context, source):
    if source:
        converter = WEBPImageConverter()
        class_name = source.__class__.__name__

        try:
            file_obj = source.file
        except:
            file_obj = None

        if class_name == 'Image' and hasattr(source, 'file'):
            converter.init(source.file.name, source.file.storage, file_obj=file_obj)
        elif class_name == 'MultiStorageFieldFile':
            converter.init(source.name, source.storage, file_obj=file_obj)
        elif class_name == 'ThumbnailFile':
            converter.init(source.name, source.storage, file_obj=file_obj)
        else:
            converter.init(source, staticfiles_storage)

        supports_webp = context.get('supports_webp', False)
        if not supports_webp or WEBP_DEBUG:
            return converter.get_url()
        return converter.get_webp_url()

    return ''


def convert(source):
    url = None
    converted_url = None
    if source:
        converter = WEBPImageConverter()
        class_name = source.__class__.__name__

        try:
            file_obj = source.file
        except:
            file_obj = None

        if class_name == 'Image' and hasattr(source, 'file'):
            converter.init(source.file.name, source.file.storage, file_obj=file_obj)
        elif class_name == 'MultiStorageFieldFile':
            converter.init(source.name, source.storage, file_obj=file_obj)
        elif class_name == 'ThumbnailFile':
            converter.init(source.name, source.storage, file_obj=file_obj)
        else:
            converter.init(source, staticfiles_storage)

        url = converter.get_url() or source.url
        converted_url = converter.get_webp_url()
    return url, converted_url


@register.filter
def webp_url(source, alias=None):
    """
    Return the webp url for a source file or for thumbnail
    using an aliased set of thumbnail options.

    If no matching alias is found, returns an empty string.

    Example usage::
        <img src="{{ person.photo|webp_url }}" alt="">
        or
        <img src="{{ person.photo|webp_url:'small' }}" alt="">
    """
    if alias:
        try:
            from easy_thumbnails.files import get_thumbnailer
            from easy_thumbnails.conf import settings
            source = get_thumbnailer(source)[alias]
        except ImportError:
            pass
        except Exception as e:
            if settings.THUMBNAIL_DEBUG:
                raise e
    url, converted_url = convert(source)
    return converted_url if converted_url and converted_url != url else ''


@register.simple_tag
def webp_picture(source, **kwargs):
    kwargs_text = ' '.join([''] + [f'{key}="{value}"' for key, value in kwargs.items()])

    url, converted_url = convert(source)
    if converted_url and converted_url != url:
        return mark_safe(f'<picture><source srcset="{converted_url}" type="image/webp"/><img src="{url}"{kwargs_text}/></picture>')
    else:
        return mark_safe(f'<img src="{url}"{kwargs_text}/>')


@register.simple_tag
def webp_imageset(source):
    url, converted_url = convert(source)
    mimetype = mimetypes.guess_type(url)[0]

    if converted_url and converted_url != url:
        return mark_safe(f'image-set(url("{converted_url}") type("image/webp"), url("{url}") type("{mimetype}"))')
    else:
        return mark_safe(f'url("{url}")')


@register.simple_tag
def webp_imageset_resolution(**kwargs):
    urls = []
    for resolution, source in kwargs.items():
        resolution = resolution[::-1]
        url, converted_url = convert(source)
        mimetype = mimetypes.guess_type(url)[0]

        if converted_url and converted_url != url:
            urls.append(f'url("{converted_url}") {resolution} type("image/webp")')
            urls.append(f'url("{url}") {resolution} type("{mimetype}")')
        else:
            urls.append(f'url("{url}") {resolution}')

    return mark_safe('image-set(' + ', '.join(urls) + ')')
