
from django.urls import path
from . import views

app_name = "users_app"
urlpatterns = [
    path('register/', 
        views.UserRegisterCreateView.as_view(),
        name='user_register',
    ),
    path('login/', 
        views.LoginUser.as_view(),
        name='user_login',
    ),
    path('logout/', 
        views.LogoutView.as_view(),
        name='user_logout',
    ),
    path('update-pass/', 
        views.ChangePassword.as_view(),
        name='update_pass',
    ),
    path('verification/<pk>/', 
        views.codeVerification.as_view(),
        name='code',
    ),
    
]