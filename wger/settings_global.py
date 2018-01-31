# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import re
import sys
'''
This file contains the global settings that don't usually need to be changed.
For a full list of options, visit:
    https://docs.djangoproject.com/en/dev/ref/settings/
'''

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))

#
# Application definition
#
SITE_ID = 1
ROOT_URLCONF = 'wger.urls'
WSGI_APPLICATION = 'wger.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'social_django',

    # Uncomment the next line to enable the admin:
    'django.contrib.admin',

    # Apps from wger proper
    'wger.core',
    'wger.manager',
    'wger.weight',
    'wger.exercises',
    'wger.nutrition',
    'wger.software',
    'wger.utils',
    'wger.config',
    'wger.gym',
    'wger.email',

    # reCaptcha support, see https://github.com/praekelt/django-recaptcha
    'captcha',

    # The sitemaps app
    'django.contrib.sitemaps',

    # Django mobile
    'django_mobile',

    # thumbnails
    'easy_thumbnails',

    # CSS/JS compressor
    'compressor',

    # REST-API
    'tastypie',
    'rest_framework',
    'rest_framework.authtoken',

    # Breadcrumbs
    'django_bootstrap_breadcrumbs',

    # CORS
    'corsheaders',

    # django-bower for installing bower packages
    'djangobower',
)


# added list of external libraries to be installed by bower
BOWER_INSTALLED_APPS = (
      "bootstrap#^3.3.7",
      "components-font-awesome#^4.7.0",
      "d3#4",
      "DataTables#^1.10.16",
      "shariff#^2.1.1",
      "sortablejs#1.4.x",
      "tinymce-dist#^4.7.4",
      "jquery#2.1.x",
      "metrics-graphics#^2.12.0",
      "devbridge-autocomplete#1.2.x"
)

MIDDLEWARE_CLASSES = (
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # Javascript Header. Sends helper headers for AJAX
    'wger.utils.middleware.JavascriptAJAXRedirectionMiddleware',

    # Custom authentication middleware. Creates users on-the-fly
    # for certain paths
    'wger.utils.middleware.WgerAuthenticationMiddleware',

    # Send an appropriate Header so search engines don't index pages
    'wger.utils.middleware.RobotsExclusionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',

    'social_django.middleware.SocialAuthExceptionMiddleware', # <--
    

    # Django mobile
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2', # <--
    'social_core.backends.twitter.TwitterOAuth', # <--
    'social_core.backends.google.GoogleOAuth2', # <--
    'social_core.backends.facebook.FacebookOAuth2', # <--
    'django.contrib.auth.backends.ModelBackend',
    'wger.utils.helpers.EmailAuthBackend'
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'wger.utils.context_processor.processor',

                # Django
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',

                # Django mobile
                'django_mobile.context_processors.flavour',

                # Setting of Template Context Processors for Social Auth
                'social_django.context_processors.backends',  # <--
                'social_django.context_processors.login_redirect', # <--

                # Breadcrumbs
                'django.template.context_processors.request'
            ],
            'loaders': [
                # Django mobile
                'django_mobile.loader.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'debug':
            False
        },
    },
]

# Store the user messages in the session
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # added BowerFinder to list of static file finders
    'djangobower.finders.BowerFinder',

    # Django compressor
    'compressor.finders.CompressorFinder',
)

#
# Email
#
EMAIL_SUBJECT_PREFIX = '[wger] '
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

#
# Login
#
LOGIN_URL = '/user/login'
LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

#
# Internationalization
#
USE_TZ = True
USE_I18N = True
USE_L10N = True

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None

# Restrict the available languages
LANGUAGES = (
    ('en', 'English'),
    ('de', 'German'),
    ('bg', 'Bulgarian'),
    ('es', 'Spanish'),
    ('ru', 'Russian'),
    ('nl', 'Dutch'),
    ('pt', 'Portuguese'),
    ('el', 'Greek'),
    ('cs', 'Czech'),
    ('sv', 'Swedish'),
    ('no', 'Norwegian'),
)

# Default language code for this installation.
LANGUAGE_CODE = 'en'

# All translation files are in one place
LOCALE_PATHS = (os.path.join(SITE_ROOT, 'locale'), )

FLAVOURS_STORAGE_BACKEND = 'session'


#
# Logging
# See http://docs.python.org/library/logging.config.html
#
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
    },
    'loggers': {
        'wger': {
            'handlers': ['console'],
            'level': 'DEBUG',
        }
    }
}

#
# ReCaptcha
#
RECAPTCHA_USE_SSL = True

#
# Cache
#
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'wger-cache',
        'TIMEOUT': 30 * 24 * 60 * 60,  # Cache for a month
    }
}

#
# Easy thumbnails
#
THUMBNAIL_ALIASES = {
    '': {
        'micro': {
            'size': (30, 30)
        },
        'micro_cropped': {
            'size': (30, 30),
            'crop': 'smart'
        },
        'thumbnail': {
            'size': (80, 80)
        },
        'thumbnail_cropped': {
            'size': (80, 80),
            'crop': 'smart'
        },
        'small': {
            'size': (200, 200)
        },
        'small_cropped': {
            'size': (200, 200),
            'crop': 'smart'
        },
        'medium': {
            'size': (400, 400)
        },
        'medium_cropped': {
            'size': (400, 400),
            'crop': 'smart'
        },
        'large': {
            'size': (800, 800),
            'quality': 90
        },
        'large_cropped': {
            'size': (800, 800),
            'crop': 'smart',
            'quality': 90
        },
    },
}

#
# Django compressor
#
STATIC_ROOT = ''
STATIC_URL = '/static/'

# The default is not DEBUG, override if needed
# COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ('compressor.filters.css_default.CssAbsoluteFilter',
                        'compressor.filters.cssmin.rCSSMinFilter')
COMPRESS_ROOT = STATIC_ROOT

# BOWER binary
if sys.platform.startswith('win32'):
    BOWER_PATH = os.path.join('node_modules', '.bin', 'bower.cmd')
else:
    BOWER_PATH = os.path.join('node_modules', '.bin', 'bower')

#
# Django Rest Framework
#
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('wger.utils.permissions.WgerPermission', ),
    'PAGINATE_BY':
    20,
    # Allow client to override, using `?limit=xxx`.
    'PAGINATE_BY_PARAM':
    'limit',
    'TEST_REQUEST_DEFAULT_FORMAT':
    'json',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    )
}

#
# CORS headers: allow all hosts to access the API
#
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'

# Ignore these URLs if they cause 404
#
IGNORABLE_404_URLS = (re.compile(r'^/favicon\.ico$'), )

# Application specific configuration options
#
# Consult docs/settings.rst for more information
#
WGER_SETTINGS = {
    'USE_RECAPTCHA': False,
    'REMOVE_WHITESPACE': False,
    'ALLOW_REGISTRATION': True,
    'ALLOW_GUEST_USERS': True,
    'EMAIL_FROM': 'wger Workout Manager <wger@example.com>',
    'TWITTER': False
}

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

SOCIAL_AUTH_TWITTER_AUTH_EXTRA_ARGUMENTS = {'force_login': 1} 
SOCIAL_AUTH_FACEBOOK_AUTH_EXTRA_ARGUMENTS = {'auth_type': 'reauthenticate'}

SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('FB_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('FB_SECRET')

SOCIAL_AUTH_GITHUB_KEY = os.getenv('GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = os.getenv('GITHUB_SECRET')

SOCIAL_AUTH_TWITTER_KEY = os.getenv('TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.getenv('TWITTER_SECRET')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_SECRET')
