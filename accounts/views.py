from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from affiliate_program.models import Promoter, Code
from main.models import Client

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid user or password')
        else:
            messages.error(request, 'User does not exist or password is incorrect')
            print(form.errors)
    else:
        form = AuthenticationForm()
    return render(request, 'affiliate_login.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'affiliate_program.html')

@login_required
def dashboard(request):
    user = request.user

    # Get the promoter associated with the logged-in user
    promoter = Promoter.objects.get(email=user.email)

    # Get the promoter's code
    code = Code.objects.get(user=promoter)

    # Get all clients who used this promoter's referral code (string match)
    clients = Client.objects.filter(ref_code=code)

    return render(request, 'dashboard.html', {
        'promoter': promoter,
        'clients': clients,
        'code': code,
    })

@login_required
def request_cashout(request):
    promoter = Promoter.objects.get(username=request.user.username)

    if promoter.balance == 0:
        messages.warning(request, "❌ You cannot request a cashout with a balance of 0.")
        return redirect('dashboard')

    if promoter.cashout_status == 'None':
        promoter.cashout_status = 'Requested'
        promoter.save(update_fields=['cashout_status'])
        messages.success(request, "Cashout request sent successfully.")
    else:
        messages.warning(request, "You already have a pending or processed cashout.")
    return redirect('dashboard')

