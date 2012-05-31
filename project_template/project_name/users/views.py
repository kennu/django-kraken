from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from models import UserProfile

def profile(request, id):
    """
    User profile page.
    """
    user = get_object_or_404(User, id=id)
    try:
        profile = user.get_profile()
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    return render(request, 'users/profile.html', {
        'user': user,
        'profile': profile,
    })

def profile_me(request):
    return redirect(reverse('user_profile', kwargs={'id':request.user.id}) if request.user.is_authenticated() else reverse('home'))
