import setuptools
from django_webp import __version__

with open('README.rst') as file:
    long_description = file.read()


setuptools.setup(
    name='js-webp',
    version=__version__,
    author=u'Andre Farzat',
    author_email='andrefarzat@gmail.com',
    packages=setuptools.find_packages(),
    url='http://pypi.python.org/pypi/django-webp/',
    license='MIT',
    description='Returns a webp image instead of jpg, gif or png to browsers which have support',
    long_description=long_description,
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.5',
)
