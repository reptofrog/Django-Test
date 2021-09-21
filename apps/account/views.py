from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm
from functools import wraps
from django.contrib.auth.forms import (
    AuthenticationForm,
)

#////////////////////////////////////////////////////////////
#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#
# Helper functions

def require_http_methods_redirect(request_method_list, redirect_to=None):
    def decorator(func):
        @wraps(func)
        def inner(request, *args, **kwargs):
            if request.method not in request_method_list:
                if redirect_to is not None:
                    return redirect(redirect_to)
                else:
                    response = HttpResponseNotAllowed(request_method_list)
                log_response(
                    'Method Not Allowed (%s): %s', request.method, request.path,
                    response=response,
                    request=request,
                )
                return response
            return func(request, *args, **kwargs)
        return inner
    return decorator


def not_logged_in(user):
  return not user.is_authenticated

#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#//\\#
#////////////////////////////////////////////////////////////


@user_passes_test(not_logged_in, login_url='account:profile', redirect_field_name=None)
@require_http_methods(['GET', 'POST'])
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('account:profile')
    
    if request.method == 'GET':
        form = AuthenticationForm()

    return render(request, 'account/blocks/login.html', {'form': form})



@login_required(redirect_field_name=None)
@require_http_methods_redirect(['POST'], redirect_to='account:profile')
def logout_view(request):
    logout(request)
    return redirect('account:login')


@user_passes_test(not_logged_in, login_url='account:profile', redirect_field_name=None)
@require_http_methods(['GET', 'POST'])
def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('account:login')
    
    if request.method == 'GET':
        form = CustomUserCreationForm()

    return render(request, 'account/blocks/signup.html', {'form': form})


@login_required
@require_http_methods(['GET'])
def profile_view(request):
    return render(request, 'account/blocks/profile.html')