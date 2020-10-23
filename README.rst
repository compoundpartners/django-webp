django-webp
===========

Returns a webp image instead of jpg, gif or png to browsers which have
support.

|Build Status| |Coverage Status|


Usage for static files
-----

Load the ``webp`` module in your template and use the ``webp``
templatetag to point to the image you want to convert.

.. code:: html

    {% load webp %}

    {# Use webp as you would use static templatetag #}
    <img src="{% webp 'path/to/your/image.png' %}" alt="image" />
    <!--
    If the browser has support, generates:
    <img src="/static/path/to/your/image.webp" alt="image" />

    else, generates:
    <img src="/static/path/to/your/image.png" alt="image" />
    -->

Usage for filer images
-----

Load the ``webp`` module in your template and use the ``webp``
templatetag to point to the image you want to convert.

.. code:: html

    {% load webp %}

    <img src="{% webp person.visual %}" alt="person" />

    {# or #}

    <img src="{% webp person.visual.file %}" alt="person" />

Usage for thumnails
-----

.. code:: html

    {% thumbnail person.visual "200x200" as im %}
    <img src="{{ im.url }}{% if supports_webp %}.webp{% endif %}" alt="{{ person.name }}">

    {# or #}

    <img src="{% thumbnail person.visual "200x200" %}{% if supports_webp %}.webp{% endif %}" alt="{{ person.name }}">

Installation
------------

First of all, you must install the webp support. In ubuntu you can
install via apt-get:

.. code:: sh

    apt-get install libwebp-dev

Please, check `the official guide`_ for the other systems.

Then, install ``django-webp``.

.. code:: sh

    pip install django-webp

add it to ``INSTALLED_APPS`` configuration

.. code:: python

    INSTALLED_APPS = (
        'django.contrib.staticfiles',
        'django_webp',
        '...',
    )

add the django\_webp context processor

.. code:: python

    TEMPLATES = [
        {
            '...'
            'OPTIONS': {
                'context_processors': [
                    '...',
                    'django_webp.context_processors.webp',
                ],
            },
        },
    ]

Possible problems
-----------------

``django-webp`` uses ``Pillow`` to convert the images. If you’ve
installed the ``libwebp-dev`` after already installed ``Pillow``, it’s
necessary to uninstall and install it back because it needs to be
compiled with it.

