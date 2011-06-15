# Django settings for the reporter project.

import os
import logging

from django.utils.functional import lazy


# Make filepaths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

ROOT_PACKAGE = os.path.basename(ROOT)


DEBUG = False
TEMPLATE_DEBUG = DEBUG

## Log settings
LOG_LEVEL = logging.DEBUG
HAS_SYSLOG = True
SYSLOG_TAG = "http_app_reporter"
LOGGING_CONFIG = None
LOGGING = {
    'loggers': {
        'i.sphinx': {'level': logging.INFO},
    },
}

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ROUTERS = ('website_issues.db.DatabaseRouter',
                    'multidb.MasterSlaveRouter',)
SLAVE_DATABASES = []

# Caching
#CACHE_BACKEND = 'caching.backends.memcached://127.0.0.1:11211/'
CACHE_DEFAULT_PERIOD = CACHE_MIDDLEWARE_SECONDS = 60 * 5  # 5 minutes
CACHE_COUNT_TIMEOUT = 60  # seconds
CACHE_PREFIX = CACHE_MIDDLEWARE_KEY_PREFIX = 'reporter:'
# L10n

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-US'

# Site ID.
# Site 1 is the desktop site, site == MOBILE_SITE_ID is the mobile site. This
# is set automatically in input.middleware.MobileSiteMiddleware according to
# the request domain.
DESKTOP_SITE_ID = 1
MOBILE_SITE_ID = 2
# The desktop version is the default.
SITE_ID = DESKTOP_SITE_ID

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Accepted locales
INPUT_LANGUAGES = ('ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'en-US', 'es',
                   'fr', 'fy-NL', 'ga-IE', 'gl', 'he', 'hr', 'hu', 'id', 'it',
                   'ja', 'ko', 'nb-NO', 'nl', 'pl', 'pt-PT', 'ro', 'ru', 'sk',
                   'sl', 'sq', 'uk', 'vi', 'zh-TW', 'zh-CN')
RTL_LANGUAGES = ('ar', 'he',)  # ('fa', 'fa-IR')
# Fallbacks for locales that are not recognized by Babel. Bug 596981.
BABEL_FALLBACK = {'fy-nl': 'nl'}


# Override Django's built-in with our native names
class LazyLangs(dict):
    def __new__(self):
        from product_details import product_details
        return dict([(lang.lower(), product_details.languages[lang]['native'])
                     for lang in INPUT_LANGUAGES])
LANGUAGES = lazy(LazyLangs, dict)()

LANGUAGE_URL_MAP = dict((i[:2], i) for i in INPUT_LANGUAGES if '-' in i)
LANGUAGE_URL_MAP.update((i.lower(), i) for i in INPUT_LANGUAGES)

# Paths that don't require a locale prefix.
SUPPORTED_NONLOCALES = ('media', 'admin')

TEXT_DOMAIN = 'messages'
STANDALONE_DOMAINS = [TEXT_DOMAIN, 'javascript']
TOWER_KEYWORDS = {'_lazy': None}

# Tells the extract script what files to look for l10n in and what function
# handles the extraction. The Tower library expects this.
DOMAIN_METHODS = {
    'messages': [
        ('apps/**.py',
            'tower.management.commands.extract.extract_tower_python'),
        ('**/templates/**.html',
            'tower.management.commands.extract.extract_tower_template'),
    ],
}


# Media

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = path('media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Ignore me!
SECRET_KEY = '^e*0du@u83$de+==+x$5k%x#+4v7&nm-_sggrr(t!&@kufz87n'

# Templates
CSRF_FAILURE_VIEW = '%s.urls.handler_csrf' % ROOT_PACKAGE
TEMPLATE_DIRS = (path('templates'),)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.core.context_processors.csrf',

    'input.context_processors.i18n',
    'input.context_processors.input',
    'input.context_processors.mobile',
    'input.context_processors.opinion_types',

    'search.context_processors.product_versions',
    'jingo_minify.helpers.build_ids',
)

# Bundles is a dictionary of two dictionaries, css and js, which list css files
# and js files that can be bundled together by the jingo-minify app.
MINIFY_BUNDLES = {
    'css': {
        'common': (
            'css/libs/reset-min.css',
            'css/libs/jquery-ui.css',
            'css/input.css',
        ),
        'common_mobile': (
            'css/libs/reset-min.css',
            'css/input-mobile.css',
        ),

        # old styles for submission pages
        'common_old': (
            'css/reporter.css',
        ),
        'mobile_old': (
            'css/reporter.css',
            'css/mobile.css',
        ),

        # Feedback for Firefox release versions
        'feedback': (
            'css/libs/reset2.css',
            'css/feedback.css',
        ),
        'feedback-mobile': (
            'css/libs/reset-min.css',
            'css/feedback-mobile.css',
        ),
    },
    'js': {
        'common': (
            'js/libs/jquery.min.js',
            'js/libs/jquery-ui.min.js',
            'js/libs/jquery.cookie.js',
            'js/init.js',
            'js/input.js',
            'js/search.js',

            # Time-based charts
            'js/libs/highcharts.src.js',
            'js/dashboard.js',
        ),
        'common_mobile': (
            'js/libs/jquery.min.js',
            'js/input-mobile.js',
        ),

        # old scripts for submission pages (desktop and mobile)
        'common_old': (
            'js/libs/jquery.min.js',
            'js/libs/jquery.NobleCount.js',
            'js/init.js',
            'js/reporter.js',
        ),

        # Release versions feedback
        'feedback': (
            'js/libs/jquery.min.js',
            'js/init.js',
            'js/feedback.js',
        ),
        'feedback-mobile': (
            'js/feedback-mobile.js',
        ),
    },
}
JAVA_BIN = '/usr/bin/java'


def JINJA_CONFIG():
    import jinja2
    config = {'extensions': ['tower.template.i18n', 'jinja2.ext.loopcontrols',
                             'jinja2.ext.with_', 'caching.ext.cache'],
              'finalize': lambda x: x if x is not None else ''}
    return config

MIDDLEWARE_CLASSES = (
    'input.middleware.MobileSiteMiddleware',
    'input.middleware.LocaleURLMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    'commonware.middleware.FrameOptionsHeader',
)

ROOT_URLCONF = '%s.urls' % ROOT_PACKAGE

INSTALLED_APPS = [
    'input',  # comes first so it always takes precedence.

    'api',
    'feedback',
    'myadmin',
    'search',
    'swearwords',
    'themes',
    'website_issues',

    'annoying',
    'cronjobs',
    'jingo_minify',
    'product_details',
    'tower',
    'djcelery',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
]

# Where to store product details
PROD_DETAILS_DIR = path('lib/product_details_json')

# Term filter options
MIN_TERM_LENGTH = 3
MAX_TERM_LENGTH = 25

# Number of items to show in the "Trends" box and Messages box.
MESSAGES_COUNT = 10
TRENDS_COUNT = 10

# Sphinx Search Index
SPHINX_HOST = '127.0.0.1'
SPHINX_PORT = 3314
SPHINXQL_PORT = 3309
SPHINX_SEARCHD = 'searchd'
SPHINX_INDEXER = 'indexer'
SPHINX_CATALOG_PATH = path('tmp/data/sphinx')
SPHINX_LOG_PATH = path('tmp/log/searchd')
SPHINX_CONFIG_PATH = path('configs/sphinx/sphinx.conf')

TEST_SPHINX_PORT = 3414
TEST_SPHINXQL_PORT = 3409
TEST_SPHINX_CATALOG_PATH = path('tmp/test/data/sphinx')
TEST_SPHINX_LOG_PATH = path('tmp/test/log/searchd')

SEARCH_MAX_RESULTS = 1000
SEARCH_PERPAGE = 20  # results per page
SEARCH_MAX_PAGES = SEARCH_MAX_RESULTS / SEARCH_PERPAGE

TEST_RUNNER = 'test_utils.runner.RadicalTestSuiteRunner'

CLUSTER_SIM_THRESHOLD = 2

## Celery
BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
BROKER_VHOST = "input"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_CONNECTION_TIMEOUT = 0.1
CELERY_RESULT_BACKEND = 'amqp'
CELERY_IGNORE_RESULT = True
CELERY_IMPORTS = ('django_arecibo.tasks',)

import djcelery
djcelery.setup_loader()

## API
TSV_EXPORT_DIR = path('media/data')

# URL for reporting arecibo errors too. If not set, won't be sent.
ARECIBO_SERVER_URL = ""

## ElasticSearch
ES_HOSTS = []
ES_INDEX = 'input'
ES_DISABLED = True
## FEATURE FLAGS:
# Setting this to False allows feedback to be collected from any user agent.
# (good for testing)
ENFORCE_USER_AGENT = True
DISABLE_TERMS = False
