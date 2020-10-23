from aldryn_client import forms

class Form(forms.BaseForm):
    def to_settings(self, data, settings):
        settings['TEMPLATES'][0]['OPTIONS']['context_processors'].append('django_webp.context_processors.webp')
        return settings
