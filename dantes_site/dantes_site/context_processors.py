import os

from django.http import HttpRequest


def site_globals(request: HttpRequest) -> dict:
    if os.environ.get("DANTES_ENV") == 'personal':
        return {
            'site_name': 'DantesDoesThings',
            'site_email': 'dantesdoesthings@gmail.com',
        }
    return {
        'site_name': 'M Baramidze',
        'site_email': 'm.baramid@gmail.com',
    }
