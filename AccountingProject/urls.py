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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from AccountingApp import views

# r'^(?i)admin/'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^(?i)contact-us/', views.contactus, name='contact-us'),
    url(r'^(?i)accounting/', include('AccountingApp.urls')),
    url(r'^(?i)accounts/', include('users_accounts.urls', namespace='users_accounts')),
    url(r'^(?i)accounts/', include('django.contrib.auth.urls')),
    url(r'^(?i)organizations/', include('organizations.urls', namespace='organizations')),
    url(r'^(?i)admin/', admin.site.urls),
]

