from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():

            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            content = f"Message from {name} ({email}):\n\n{form.cleaned_data['content']}"

            subject = f"Client {name}"
            from_email = email  # Sender's email
            recipient_list = ['info@dentalhavens.com']  # Replace with your email address

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
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
