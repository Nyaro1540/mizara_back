from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    PasswordResetRequestView, 
    PasswordResetConfirmView,
    ProfileCollecteurView,
    CompleteProfileCollecteurView
)

from django.urls import path
from .views import upload_profile_picture  # Assurez-vous que cette vue est définie

urlpatterns = [
    path('upload-profile-picture/', upload_profile_picture, name='upload_profile_picture'),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile-collecteur/', ProfileCollecteurView.as_view(), name='profile_collecteur'),
    path('complete-profile-collecteur/', CompleteProfileCollecteurView.as_view(), name='complete_profile_collecteur'),
]
