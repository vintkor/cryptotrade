try:
    from cryptotrade.prod_settings import *
except:

    import os

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SECRET_KEY = 'pwd&f_5o)&4ym+*3m$bs(mj^+6$3%z&shzym#frehxigy4y42!'

    DEBUG = True

    ALLOWED_HOSTS = ['*']
    INTERNAL_IPS = '127.0.0.1'

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'debug_toolbar',
        'mptt',
        'ckeditor',
        'ckeditor_uploader',

        'user_profile',
        'binary_tree',
        'linear_tree',
        'news',
        'packages',
        'finance',
        'geo',
        'shares',
        'awards',
        'dashboard',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

    ROOT_URLCONF = 'cryptotrade.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = 'cryptotrade.wsgi.application'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    AUTH_USER_MODEL = 'user_profile.User'
    AUTHENTICATION_BACKENDS = (
        "django.contrib.auth.backends.ModelBackend",
    )

    LANGUAGE_CODE = 'ru-RU'

    TIME_ZONE = 'Europe/Kiev'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = False

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "static"),
    )

    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    CKEDITOR_UPLOAD_PATH = 'uploads/'
    CKEDITOR_CONFIGS = {
        'default': {
            # 'skin': 'moono',
            # 'skin': 'office2013',
            'toolbar_Basic': [
                ['Source', '-', 'Bold', 'Italic']
            ],
            'toolbar_YourCustomToolbarConfig': [
                {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
                {'name': 'clipboard',
                 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
                {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
                {'name': 'basicstyles',
                 'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
                {'name': 'paragraph',
                 'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv',
                           '-',
                           'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                           'Language']},
                {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
                {'name': 'insert',
                 'items': ['Image', 'Youtube', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak',
                           'Iframe']},
                '/',
                {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
                {'name': 'colors', 'items': ['TextColor', 'BGColor']},
                {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
                {'name': 'about', 'items': ['About']},
                {'name': 'yourcustomtools', 'items': ['Preview', 'Maximize', ]},
            ],
            'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
            # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
            # 'height': 291,
            # 'width': '100%',
            # 'filebrowserWindowHeight': 725,
            # 'filebrowserWindowWidth': 940,
            # 'toolbarCanCollapse': True,
            # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
            'tabSpaces': 4,
            'extraPlugins': ','.join([
                'uploadimage',  # the upload image feature
                # your extra plugins here
                'div',
                'autolink',
                'autoembed',
                'embedsemantic',
                'autogrow',
                # 'devtools',
                'widget',
                'lineutils',
                'clipboard',
                'dialog',
                'dialogui',
                # 'youtube',
                'elementspath'
            ]),
        }
    }

