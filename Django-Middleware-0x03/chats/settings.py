# 0x03-MessagingApp-Django/0x03-MessagingApp-Django/settings.py

MIDDLEWARE = [
    # Django default middleware (example placeholders)
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Custom middlewares
    'chats.middleware.RequestLoggingMiddleware',
    'chats.middleware.RestrictAccessByTimeMiddleware',
]

# Minimal settings to make Django project structure valid
INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.contenttypes', 'chats']
ROOT_URLCONF = '0x03-MessagingApp-Django.urls'
SECRET_KEY = 'placeholder-secret-key'
DEBUG = True
ALLOWED_HOSTS = ['*']
