"""
Django settings for mora_inscribe project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-#d#nmtr(6mow$rs0z*dqga!x)vg(kphllkiyf#%man)%%%h-#s'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = os.getenv("DEBUG",'False').lower() == 'true'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ic_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mora_inscribe.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'mora_inscribe.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# 读写分离配置 
#     https://www.cnblogs.com/LiaJi/p/17346826.html#tid-sFFSFT
#     https://blog.csdn.net/vlking/article/details/127015680
mysql_db_option = {}
mysql_db_option_ca = os.getenv("MYSQL_SSL_CA",'') or ""
if mysql_db_option_ca:
    mysql_db_option['ssl'] = mysql_db_option_ca
db_pool_size = os.getenv("DB_POOL_SIZE") or '5'
pool_size = os.getenv("POOL_SIZE") or "20"
max_overflow = os.getenv("MAX_OVERFLOW") or "8"
DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     # BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        # 数据库引擎
        # 'ENGINE': 'django.db.backends.mysql',       
        'ENGINE': 'dj_db_conn_pool.backends.mysql',
        # 重写 mysql 连接库实现连接池
        # 'ENGINE': 'db_pool.mysql',
        # 数据库名，Django不会帮你创建，需要自己进入数据库创建。
        'NAME': os.getenv("DB_DATABASE") or "",     
        # 设置的数据库用户名
        'USER': os.getenv("DB_USERNAME") or "",     
        # 设置的密码
        'PASSWORD': os.getenv("DB_PASSWORD") or "", 
        # 本地主机或数据库服务器的ip
        'HOST': os.getenv("DB_HOST") or "",         
        # 数据库使用的端口
        'PORT': os.getenv("DB_PORT") or "",   
        'CHARSET':os.getenv("DB_CHARSET") or "utf8mb4",
        'TIME_ZONE':'Asia/Shanghai',

        'OPTIONS': mysql_db_option,
        # 'CONN_MAX_AGE': 600,    # 如果使用 db_pool.mysql 绝对不能设置此参数，否则会造成使用连接后不会快速释放到连接池，从而造成连接池阻塞
        # 数据库连接池大小，mysql 总连接数大小为：连接池大小 * 服务进程数
        # 'DB_POOL_SIZE': int(db_pool_size),     # 默认 5 个

        # dj_db_conn_pool
        'POOL_OPTIONS' : {
            # POOL_SIZE（连接池容量）
            'POOL_SIZE': int(pool_size),
            # MAX_OVERFLOW（连接池容量向上浮动最大值）
            'MAX_OVERFLOW': int(max_overflow),
            # 目前连接池限制用户传入的连接池配置为：POOL_SIZE（连接池容量）、MAX_OVERFLOW（连接池容量向上浮动最大值） 
            # 这两个参数包含在 POOL_OPTIONS 内，例如下面的配置，default 的连接池常规容量为10个连接，最大浮动10个， 
            # 即为：在 default 连接池创建后，随着程序对连接池的请求，连接池内连接将逐步增加到10个，如果在连接池内连接 
            # 全部用光后，程序又请求了第11个连接，此时的连接池容量将短暂超过 POOL_SIZE，但最大不超过 POOL_SIZE + MAX_OVERFLOW， 
            # 如果程序请求 default 数据库的连接数量超过 POOL_SIZE + MAX_OVERFLOW，那么连接池将一直等待直到程序释放连接， 
            # 请注意线程池对数据库连接池的使用，如果线程池大于连接池，且线程无主动释放连接的动作，可能会造成其他线程一直阻塞
            # 重新连接的时间
            'RECYCLE':10,
        },

        # 'OPTIONS': {
        #     'ssl': {
        #         # # 在macOS 运行 ，自带的证书路径
        #         # # MYSQL_ATTR_SSL_CA=/etc/ssl/cert.pem
        #         # # 在Docker 运行 ，自带的证书路径
        #         # MYSQL_ATTR_SSL_CA=/etc/ssl/certs/ca-certificates.crt
        #         # # 在centos 运行 ，自带的证书路径
        #         # # MYSQL_ATTR_SSL_CA=/etc/pki/tls/certs/ca-bundle.crt
        #         # CA证书的路径。这是用于验证MySQL服务器证书的根证书
        #         'ca': '/path/to/ca-cert.pem',
        #         # 客户端私钥的路径。这是用于身份验证的私钥
        #         'key': '/path/to/client-key.pem',
        #         # 客户端证书的路径。这是用于身份验证的公钥证书
        #         'cert': '/path/to/client-cert.pem',
        #     }
        # },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'

# USE_I18N = True

# USE_TZ = True
# 设置为中文
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'


USE_I18N = True

USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
