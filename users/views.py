from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import MyUserCreationForm, UserUpdateForm, ProfileUpdateForm


def register(request):
    if request.method == 'POST':
        user_form = MyUserCreationForm(request.POST)

        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Profilo di {username} creato! Ora puoi accedere e modificare le tue preferenze.')
            return redirect('users-login')
    else:
        user_form = MyUserCreationForm()
    return render(request, 'users/register.html', {'u_form': user_form})


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form.save()
            username = user.username
            messages.success(request, f'Profilo di {username} aggiornato correttamente!')
            return redirect('users-profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.user_profile)

    context = {
        'u_form': user_form,
        'p_form': profile_form
    }

    return render(request, 'users/profile.html', context)

