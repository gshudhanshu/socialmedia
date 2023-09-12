from django.urls import path
from . import views

urlpatterns = [
    path('profile', views.ProfileView.as_view(), name='user-profile-detail'),
    path('profile/edit', views.EditProfileView.as_view(), name='edit-profile'),
    path('profile/<int:user_id>', views.ProfileView.as_view(), name='friend-profile-detail'),

]
