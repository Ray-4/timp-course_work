from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrForm, EditUserForm, EditProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User
from django.views.generic import ListView
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import authentication, permissions


# регистрация
def register(request):
    if request.method == 'POST':
        form = RegistrForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Спасибо, {username}. Ваш аккаунт был создан')
            return redirect('login')

    else:
        form = RegistrForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST,
                                         request.FILES,
                                         instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Ваша информация была обновлена')
            return redirect('edit_profile')

    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'users/edit_profile.html', context)


# Это представление создает REST API. Каждый раз, когда к REST API обращаются
# через кнопку jQuery, аутентифицированный пользователь добавляется / удаляется из
# списка пользователей, которые следили за конкретным пользователем.

class FollowUser(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None, user=None, username=None):
        obj = get_object_or_404(User, username=username)
        prof_obj = get_object_or_404(Profile, user=obj)
        authenticated_user = self.request.user
        updated = False
        followed = False
        if authenticated_user.is_authenticated:
            if authenticated_user in prof_obj.followers.all():
                followed = False
                prof_obj.followers.remove(authenticated_user)
                follower_count = prof_obj.followers.count()
                button = 'Подписаться'
            else:
                followed = True
                prof_obj.followers.add(authenticated_user)
                follower_count = prof_obj.followers.count()
                button = 'Отписаться'
            updated = True
        data = {
            "updated": updated,
            "followed": followed,
            "follower_count": follower_count,
            "button": button
        }
        return Response(data)


class ViewFollowers(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/user_followers.html'
    context_object_name ='profile'
    ordering = ['-date_posted']

    def get_queryset(self):
        obj = get_object_or_404(User, username=self.kwargs.get('username'))
        prof_obj = get_object_or_404(Profile, user=obj)
        return prof_obj

from .forms import AuthorizationForm, PassResetForm, ResetPassForm
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView


class AuthorizationView (LoginView):
    form_class = AuthorizationForm

class PassResetView(PasswordResetView):
    form_class = PassResetForm

class PassResetConfirmView (PasswordResetConfirmView):
    form_class = ResetPassForm

































