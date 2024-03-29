from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('register/', views.register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path('user/<str:username>/follow/', views.FollowUser.as_view(), name='user_follow'),
    path('user/<str:username>/followers/', views.ViewFollowers.as_view(), name='user_followers'),
]

urlpatterns += [
    path('login/', views.AuthorizationView.as_view(template_name='users/login.html'), name='login'),

    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    path('password_reset/', views.PassResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),


    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',
         views.PassResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
