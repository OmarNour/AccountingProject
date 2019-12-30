from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users_accounts'

urlpatterns = [
    path('login/',auth_views.LoginView.as_view(template_name="login.html"),name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('signup/', views.SignUp.as_view(), name="signup"),

    path('invitation/signup/<org_id>/<inv_id>/', views.InvitationSignUp.as_view(), name="invitation-signup"),
]
