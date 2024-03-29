# Settings for running in prod
DEBUG = False

ALLOWED_HOSTS = [
    'www.dantesdoesthings.com',
    'www.mbaramidze.com',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

MEDIA_ROOT = '/mnt/volume_nyc1_01/uploads'
MEDIA_URL = 'media/'
