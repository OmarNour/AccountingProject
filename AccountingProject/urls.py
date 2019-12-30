"""AccountingProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# from django.contrib import admin
# from django.conf.urls import include

from django.contrib import admin
from django.urls import include, path
from AccountingApp import views

# python manage.py runserver
# r'^(?i)admin/'
urlpatterns = [
    # path(r'^$', views.home, name='home'),
    # path(r'^(?i)contact-us/', views.contactus, name='contact-us'),
    path('', views.home, name='home'),
    path('contact-us/', views.contactus, name='contact-us'),
    path('accounting/', include('AccountingApp.urls')),
    path('accounts/', include('users_accounts.urls', namespace='users_accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('organizations/', include('organizations.urls', namespace='organizations')),
    path('admin/', admin.site.urls)
]

# urlpatterns = [
#     path(r'^$', views.home, name='home'),
#     path(r'^(?i)contact-us/', views.contactus, name='contact-us'),
#     path(r'^(?i)accounting/', include('AccountingApp.urls')),
#     path(r'^(?i)accounts/', include('users_accounts.urls', namespace='users_accounts')),
#     path(r'^(?i)accounts/', include('django.contrib.auth.urls')),
#     path(r'^(?i)organizations/', include('organizations.urls', namespace='organizations')),
#     path(r'^(?i)admin/', admin.site.urls),
# ]
