from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Contact
from django.core.mail import send_mail

from . import views
# Create your views here.
def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['listing_id']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        #check if user has made an enquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)

            if has_contacted:
                messages.error(request,'you have already made an enquiry to this listing')
                return redirect('/listings/' + listing_id)

        contact = Contact(listing=listing, listing_id=listing_id, name=name,
                        email=email, phone=phone, message=message, user_id=user_id)

        contact.save()

        # send mail
        send_mail(
            'Property Lisiting Inquiry',
            'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
            'odetolataiwo@gmail.com',
            [realtor_email, 'admin@btre.com'],
            fail_silently=False
        ) 

        messages.success(request, "Your request has been submitted. A realtor will get to you soon.")

        return redirect('/listings/' + listing_id)
