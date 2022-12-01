from django.http import HttpRequest


def site_globals(request: HttpRequest) -> dict:
    if request.get_port() == 8001:
        return {
            'site_name': 'DantesDoesThings',
            'site_email': 'dantesdoesthings@gmail.com',
        }
    return {
        'site_name': 'M Baramidze',
        'site_email': 'm.baramid@gmail.com',
    }
