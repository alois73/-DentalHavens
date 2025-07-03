from django.shortcuts import render, redirect
from .models import Service, Client, Tour
from django.core.exceptions import ValidationError
from django.shortcuts import resolve_url
from affiliate_program.models import Code, Promoter 
from django.core.mail import send_mail
from django.contrib import messages


def home(request):
    serv = Service.objects.all()
    return render(request, 'home.html', {'serv': serv})

def services(request):
    surgery_services = Service.objects.filter(category="Surgery")
    imaging_services = Service.objects.filter(category="Imaging")
    orthopedist_services = Service.objects.filter(category="Orthopedist")
    prophylaxis_services = Service.objects.filter(category="Prophylaxis")
    therapy_services = Service.objects.filter(category='Therapy')

    context = {
        'surgery_services': surgery_services,
        'imaging_services': imaging_services,
        'orthopedist_services': orthopedist_services,
        'prophylaxis_services': prophylaxis_services,
        'therapy_services': therapy_services,
    }

    return render(request, 'services.html', context)

def register(request):
    serv = Service.objects.all()
    tours = Tour.objects.all()
    return render(request, 'registration.html', {'serv': serv, 'tours': tours})

def tour_info(request):
    return render(request, 'tirana_tour.html')

def success_view(request):
    return render(request, 'success.html')

def register_client(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        tour_option = request.POST.get('tour_option')
        custom_request = request.POST.get('custom_request')  # <- add this line
        ref_code = request.POST.get('ref_code')

        print("POST data:", request.POST)

        total_price = 0.00

        code_obj = None
        if ref_code:
            try:
                code_obj = Code.objects.get(ref_code=ref_code)
            except Code.DoesNotExist:
                print(f"Referral code '{ref_code}' not found in database.")

        try:
            client = Client.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                tour_option=tour_option,
                total_price=total_price,  # always 0.00
                ref_code=code_obj,
                custom_request=custom_request,
)

            if code_obj:
                try:
                    promoter = code_obj.user
                    promoter.exp += 1
                    promoter.save(update_fields=['exp'])
                    print(f"✅ Promoter {promoter.username} gained +1 EXP on client registration.")
                except Exception as e:
                    print("❌ Error awarding EXP to promoter on registration:", e)

            # Send email notification to admin/support
            subject = f'Client Booked: {first_name} {last_name}'
            content = f'Client booking information\n\nDetails:\n- Name: {first_name} {last_name}\n- Email: {email}\n- Phone: {phone_number}\n- Tour Option: {tour_option}'
            from_email = email
            recipient_list = ['admin@dentalhavens.com', 'info@dentalhavens.com', 'aloismucaj7@gmail.com']  # Replace with your admin/support email

            try:
                send_mail(
                    subject,
                    content,
                    from_email,  
                    recipient_list,
                    fail_silently=False,
                )
                messages.success(request, "Your message has been sent successfully!")
                return redirect('contact')
            except Exception as e:
                print(f"Error sending email: {e}")
                messages.error(request, "There was an error sending your message. Please try again.")

            return redirect(resolve_url('success_view'))

        except ValidationError as e:
            print("Validation error:", e)
        except Exception as e:
            print("Unexpected error:", e)

    serv = Service.objects.all()

    send_mail()

    return render(request, 'registration.html', {'serv': serv})

def terms_view(request):
    return render(request, 'terms.html')

def privacy_view(request):
    return render(request, 'privacy.html')

def partnership_view(request):
    return render(request, 'partnership.html')