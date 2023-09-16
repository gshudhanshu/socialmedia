from django.urls import path
from . import views
from . import api

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='user-profile-detail'),
    path('profile/edit', views.UserProfileEditView.as_view(), name='edit-profile'),
    path('profile/status', views.UpdateStatusAPI.as_view(), name='update-status'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='friend-profile-detail'),

    # REST API URLS
    path('api/profiles', api.ListProfiles.as_view(), name='api-profiles'),
    path('api/profiles/<int:user_id>', api.ViewProfile.as_view(), name='api-profile'),

]
