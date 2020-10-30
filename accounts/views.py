from django.shortcuts import render,redirect,get_object_or_404
from  .forms import SignUpForm,ProfileEditForm,UserEditForm
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .models import Profile
# Create your views here.


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request,user)
            return redirect('/accounts/profile')

    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html',{'form':form})



def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request,'accounts/profile.html',{'profile':profile})

@login_required
def edit_profile(request, id):
    profile = get_object_or_404(Profile, id=id)
    if request.method == "POST":
        user_form    = UserEditForm(request.POST, instance=request.user)
        Profile_form = ProfileEditForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and Profile_form.is_valid:
            user_form.save()
            new_profile = Profile_form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
    else:
        user_form    = UserEditForm(instance=request.user)
        Profile_form = ProfileEditForm(instance=profile)
    context = {

        'user_form':user_form,
        'Profile_form':Profile_form,
        'profile':profile,
    }
    return render(request, 'accounts/edit_profile.html', context)