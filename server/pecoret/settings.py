from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-zwxlj(*k4)vb3wgkm%grj1grx&hc%ci&vj-5)tr=e7+j92(tf0"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "django_q",
    "django_filters",
    "drf_spectacular",
    "modeltranslation",
    "generic_relations",
    "backend.apps.BackendConfig",
    "advisories.apps.AdvisoriesConfig",
    "checklists.apps.ChecklistsConfig"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "pecoret.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "pecoret.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication
AUTH_USER_MODEL = "backend.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "backend.authentication.ProjectTokenAuthentication",
    ],
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DEFAULT_PAGINATION_CLASS": "pecoret.core.pagination.PeCoReTPageNumberPagination",
    "PAGE_SIZE": 100,
    "PAGE_SIZE_QUERY_PARAM": "limit",
    "MAX_PAGINATE_BY": 200,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_THROTTLE_RATES": {"auth_flow_throttle": "7/hour"},
    "EXCEPTION_HANDLER": "pecoret.core.exceptions.pecoret_execption_handler",
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}


SPECTACULAR_SETTINGS = {
    "TITLE": "PeCoReT API",
    "DESCRIPTION": "PeCoReT API documentation",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "ENUM_GENERATE_CHOICE_DESCRIPTION": False,
    "ENUM_NAME_OVERRIDES": {
        "FindingStatus": "backend.models.finding.FindingStatus.choices",
        "AssetTaskStatus": "backend.models.checklists.tasks.AssetTaskStatus.choices",
        "Roles": "backend.models.membership.Roles.choices",
    },
}

CORS_ALLOWED_ORIGINS = ["http://localhost:8080", "http://127.0.0.1:8080"]

gettext = lambda s: s
LANGUAGES = [("en", gettext("English")), ("de", gettext("German"))]
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"

CORS_EXPOSE_HEADERS = ["Content-Disposition", "Content-Type"]
CORS_ALLOW_CREDENTIALS = True

SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# expire session after 15 minutes
SESSION_COOKIE_AGE = 15 * 60

Q_CLUSTER = {
    "name": "DjangORM",
    "workers": 2,
    "timeout": 600,
    "retry": 900,
    "attempt_count": 1,
    "max_attempts": 1,
    "ack_failures": True,
    "bulk": 10,
    "orm": "default",
}


REPORT_COMPANY_INFORMATION = {"name": "PeCoReT Project", "street": "Unkown Street"}


SITE_URLS = {
    "PASSWORD_RESET": "/reset-password/{uid}/{token}",
    "ACTIVATION": "/account-activation/{uid}/{token}",
    "ADVISORY_DETAIL": "/advisories/{advisoryId}",
    "FINDING_DETAIL": "/projects/{projectId}/findings/{findingId}"
}

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
]

ENABLE_DJANGO_ADMIN_PANEL = False

SITE_NAME = "PeCoReT"
DOMAIN = "localhost:3000"
PROTOCOL = "http"

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

FALLBACK_REPORT_TEMPLATE = "default_template"

############
# Advisories
############
ADVISORY_ID_PREFIX = "pecoret"
ADVISORY_TEMPLATE = "default_template"
ADVISORY_MEMBERSHIP_DEFAULT_READ_ONLY_PERMISSION_DAYS = 120



if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        "rest_framework.renderers.BrowsableAPIRenderer"
    )

