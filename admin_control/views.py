from django.shortcuts import render, redirect
from user.models import Admin_Staff, Customer, Service_Boy
from hospital.models import Hospital_Detail
from admin_control.models import Customer_Ongoing_Trip, Customer_Service_Hist, Service_Boy_Ongoing_Trip, Service_Boy_Service_Hist

import smtplib

def admin_control(request):
    try:
        Session_ID = request.session['Admin_Staff']
        staff_admin = Admin_Staff.objects.filter(admin_staff_id=Session_ID)[0]
        customer = Customer.objects.all()
        service_boy = Service_Boy.objects.all().exclude(status=False)
        hospitals = Hospital_Detail.objects.all()
        service_boy_pending = Service_Boy.objects.filter(status=False)
        service_boy_available = Service_Boy.objects.all().exclude(available=False)
        service_boy_not_available = Service_Boy.objects.filter(available=False)
        customer_ongoing_trip = Customer_Ongoing_Trip.objects.all()
        customer_service_hist = Customer_Service_Hist.objects.filter().exclude(status='pending')
        customer_service_pending = Customer_Service_Hist.objects.filter(
            status='pending')
        service_boy_ongoing_trip = Service_Boy_Ongoing_Trip.objects.all()
        service_boy_service_hist = Service_Boy_Service_Hist.objects.all()
        #print(customer)
        #print(service_boy)
        #print(customer_ongoing_trip)
        #print(customer_service_hist)
        #print(service_boy_ongoing_trip)
        #print(service_boy_service_hist)
        return render(request, 'admin_control/index.html', {
            'active_link': 'Admin',
            'staff_admin': staff_admin,
            'customer': customer,
            'service_boy': service_boy,
            'hospitals': hospitals,
            'service_boy_pending': service_boy_pending,
            'service_boy_available': service_boy_available,
            'service_boy_not_available': service_boy_not_available,
            'customer_ongoing_trip': customer_ongoing_trip,
            'customer_service_pending': customer_service_pending,
            'customer_service_hist': customer_service_hist,
            'service_boy_ongoing_trip': service_boy_ongoing_trip,
            'service_boy_service_hist': service_boy_service_hist,
        })
    except:
        return redirect('/')


def customer(request):
    try:
        Session_ID = request.session['Admin_Staff']
        staff_admin = Admin_Staff.objects.filter(admin_staff_id=Session_ID)[0]
        customer = Customer.objects.all()
        return render(request, 'admin_control/customer.html', {
            'active_link': 'All Customers',
            'staff_admin': staff_admin,
            'customer': customer,
        })
    except:
        return redirect('/jhbo92dasdSABoiu8o08BFjkl')


def service_boys(request):
    try:
        Session_ID = request.session['Admin_Staff']
        staff_admin = Admin_Staff.objects.filter(admin_staff_id=Session_ID)[0]
        service_boy = Service_Boy.objects.all().exclude(status=False)

        # service_boy_service_hist = Service_Boy_Service_Hist.objects.filter()
        return render(request, 'admin_control/service_boy.html', {
            'active_link': 'All Service Boys',
            'staff_admin': staff_admin,
            'service_boy': service_boy,
        })
    except:
        return redirect('/jhbo92dasdSABoiu8o08BFjkl')


def pending_applications(request):
    # try:
    if(request.method == 'POST'):
        pending_ID = request.POST.get('pending_ID', '')
        #print(pending_ID)
        service_boy_pending = Service_Boy.objects.filter(
            ID=pending_ID)
        print(service_boy_pending)
        print(pending_ID)
        email = service_boy_pending[0].email
        name = service_boy_pending[0].first_name

        service_boy_pending.update(status=True, available=True, current_status="available")
        
        confirmation_message(email, pending_ID, name)

        return redirect('/jhbo92dasdSABoiu8o08BFjkl/pending_applications')
    Session_ID = request.session['Admin_Staff']
    staff_admin = Admin_Staff.objects.filter(admin_staff_id=Session_ID)[0]
    service_boy = Service_Boy.objects.filter(status=False).values()
    # service_boy_service_hist = Service_Boy_Service_Hist.objects.filter()
    return render(request, 'admin_control/pending_applications.html', {
        'active_link': 'All Service Boys',
        'staff_admin': staff_admin,
        'service_boy': service_boy,
    })
    # except:
    #     return redirect('/jhbo92dasdSABoiu8o08BFjkl')


def hospitals(request):
    try:
        Session_ID = request.session['Admin_Staff']
        staff_admin = Admin_Staff.objects.filter(admin_staff_id=Session_ID)[0]
        hospitals = Hospital_Detail.objects.all().values()

        # service_boy_service_hist = Service_Boy_Service_Hist.objects.filter()
        return render(request, 'admin_control/hospital.html', {
            'active_link': 'All Hosptails',
            'staff_admin': staff_admin,
            'hospitals': hospitals,
        })
    except:
        return redirect('/jhbo92dasdSABoiu8o08BFjkl')


def pending_service(request):
    try:
        if (request.method == 'POST'):
            customer_trip_id = request.POST.get('customer_trip_id', '')
            customer_id = request.POST.get('customer_id', '')
            service_boy = request.POST.get('service_boy', '')
            #print('customer_trip_id= ', customer_trip_id)
            #print('customer_id= ', customer_id)
            #print('service_boy= ', service_boy)
            customer_service_hist = Customer_Service_Hist.objects.filter(
                customer_trip_id=int(customer_trip_id),
                customer_id=int(customer_id)
            )
            service_boy = Service_Boy.objects.filter(ID=service_boy)[0]
            customer = Customer.objects.filter(customer_id=int(customer_id))[0]
            # #print(customer_service_hist.values())
            # #print(service_boy.values())
            # #print(customer.values())
            # #print('#')
            customer_service_hist.update(
                service_boy_id=int(service_boy.ID),
                service_boy_name=service_boy.first_name +
                ' '+service_boy.last_name,
                status='Service Boy Assigned',
            )

            service_boy_order = Service_Boy_Service_Hist(
                service_boy_trip_id=int(customer_trip_id),
                customer_id=int(customer_id),
                customer_FName=customer.first_name,
                customer_LName=customer.last_name,
                customer_mobile=customer.mobile,
                status='Assigned to Customer',
                amount=customer_service_hist[0].amount,
                service_boy_id=int(service_boy.ID),
                service_boy_name=service_boy.first_name +
                ' '+service_boy.last_name,
                date_of_booking=customer_service_hist[0].date_of_booking,
                date_of_service=customer_service_hist[0].date_of_service,
                hospital_name=customer_service_hist[0].hospital_name,
                hospital_id=customer_service_hist[0].hospital_id,
                selected_service=customer_service_hist[0].selected_service,
            )
            # service_chosen=Service_Chosen.objects.filter(
            #         service_chosen_id=confirm_order['service_chosen_id']).update(status='accepted')
            service_boy_order.save()

            return redirect('/jhbo92dasdSABoiu8o08BFjkl/pending_service')

        Session_ID = request.session['Admin_Staff']
        staff_admin = Admin_Staff.objects.filter(admin_staff_id=Session_ID)[0]

        customer_service_pending = Customer_Service_Hist.objects.filter(
            status='pending').values()

        for i in customer_service_pending:
            i['PIN'] = Hospital_Detail.objects.filter(
                hospital_id=i['hospital_id'])[0].hospital_pin
            i['available_service_boy'] = Service_Boy.objects.filter(
                status=True, pin_serve__contains=i['PIN'])

        # service_boy_service_hist = Service_Boy_Service_Hist.objects.filter()
        return render(request, 'admin_control/pending_service.html', {
            'active_link': 'Pending Services',
            'staff_admin': staff_admin,
            'customer_service_pending': customer_service_pending,
        })
    except:
        return redirect('/jhbo92dasdSABoiu8o08BFjkl')


def all_services(request):
    # try:
        Session_ID = request.session['Admin_Staff']
        staff_admin = Admin_Staff.objects.filter(admin_staff_id=Session_ID)[0]
        customer_services = Customer_Service_Hist.objects.all().values()
        for i in customer_services:
            i['service_boy_system_ID'] = Service_Boy.objects.filter(ID=str(i['service_boy_id']))[0].service_boy_id
        return render(request, 'admin_control/all_services.html', {
            'active_link': 'All Services Centre',
            'staff_admin': staff_admin,
            'customer_services': customer_services,
        })
    # except:
    #     return redirect('/jhbo92dasdSABoiu8o08BFjkl')

def admin_staff_logout(request):
    del request.session['Admin_Staff']
    return redirect('/')


# Create your views here.
# Send Message


def confirmation_message(email, service_boy_id, name):

    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.starttls()
    mail_server.login("vermakaustubh28@gmail.com", "uvbulppoaoxlwzhu")
    SUBJECT = "Welcome to isTaker"   
    TEXT = 'Hi '+str(name)+',\nwelcome to isTaker Family. Your Application Request is Completed and is Fit for our services.\nYour Service Boy ID is '+str(service_boy_id)

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    mail_server.sendmail('&&&&&&&&&&&', email, message)
