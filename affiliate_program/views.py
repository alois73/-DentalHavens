from django.shortcuts import render, redirect
from .models import Promoter, Code
import secrets
from accounts.models import User  
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
User = get_user_model() 
from django.contrib import messages

# Create your views here.
def affiliate_program(request):
    return render(request, 'affiliate_program.html')

def affiliate_register(request):
    return render(request, 'affiliate_register.html')

def generate_ref_code(length=10):
    while True:
        code = secrets.token_hex(length // 2)
        if not Code.objects.filter(ref_code=code).exists():
            return code

def register_complete(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        country = request.POST.get('country')

        User.objects.create_user(
            email=email, 
            username=username, 
            password=password
        )
        Promoter.objects.create(
            name=name,
            username=username,
            email=email,
            phone=phone,
            country=country
        )
        unique_code = generate_ref_code()
        Code.objects.create(
            ref_code=unique_code,
            user=Promoter.objects.get(email=email)
        )
        request.session['promoter_email'] = email

        # Send email notification to admin/support
        subject = f'Affiliate Registrations: {name}'
        content = f'New Affiliate\n\nDetails:\n- Name: {name}\n- User: {username}\n- Email: {email}\n- Phone: {phone}\n- Country: {country}'
        from_email = email
        recipient_list = ['admin@dentalhavens.com', 'affiliates@dentalhavens.com', 'aloismucaj7@gmail.com']  # Replace with your admin/support email

        try:
            send_mail(
                subject,
                content,
                from_email,  
                recipient_list,
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
            return redirect('affiliate_success')
        except Exception as e:
            print(f"Error sending email: {e}")
            messages.error(request, "There was an error sending your message. Please try again.")

        return redirect('affiliate_success')
    
    return redirect('affiliate_program')

def affiliate_success(request):
    email = request.session.get('promoter_email')

    if not email:
        return redirect('affiliate_program')  

    try:
        promoter = Promoter.objects.get(email=email)
        code = Code.objects.get(user=promoter)
        ref_code = code.ref_code
    except (Promoter.DoesNotExist, Code.DoesNotExist):
        ref_code = "UNKNOWN"

    request.session.pop('promoter_email', None)

    return render(request, 'affiliate_success.html', {'ref_code': ref_code})


