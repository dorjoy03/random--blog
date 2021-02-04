from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

def signup(request):
    
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('feed')

    context = {'form': form}
    return render(request, 'registration/signup.html', context)
