from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users_accounts'

urlpatterns = [
    url(r'^(?i)login/$',auth_views.LoginView.as_view(template_name="login.html"),name='login'),
    url(r'^(?i)logout/$', auth_views.LogoutView.as_view(), name="logout"),
    url(r'^(?i)signup/$', views.SignUp.as_view(), name="signup"),
]
