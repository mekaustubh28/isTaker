from django.shortcuts import render, redirect
from django.http import HttpResponse
from service.models import Confirm_Order, Service_Chosen
from user.models import Customer, Service_Boy
from hospital.models import Hospital_Detail
from admin_control.models import Admin_Control, Customer_Service_Hist, Service_Boy_Service_Hist, Customer_Ongoing_Trip, Service_Boy_Ongoing_Trip
from . import ride_complete
from service.views import convert_date_and_time, otp_generator

from datetime import datetime

# Send Message

import smtplib
import math
import random
# Create your views here.

def availability(request, ID):
    try:
        Active_Service_Boy = request.session['Active_Service_Boy']

        available = Service_Boy.objects.filter(ID=ID)
        if request.method == 'POST':
            check = request.POST.get('check', '')
            reason = request.POST.get('reason', '')
            available_check = request.POST.get('available_check', '')
            if check == 'on' and reason != '':
                available.update(available=False, reason=reason, current_status='not available')
            if check == '' and reason == '' and available_check != '':
                available.update(available=True, reason='', current_status='available')
            return redirect('/service_boy/' + str(ID) + '/availability')
        return render(request, 'service_boy/availability.html', {
                'Active_Service_Boy': Active_Service_Boy,
                'available': available[0].available
            })
    except:
        return redirect('/login')

def service_boy_dashboard(request, ID):
    try:
        request.session['once_start_ride'] = False
        order_already_placed = ''
        Active_Service_Boy = request.session['Active_Service_Boy']

        Customer_Hist = Customer_Service_Hist.objects.filter(
            service_boy_id=0,
            status='pending')

        Customer_Pending_Hist = Customer_Service_Hist.objects.filter(
            service_boy_id=ID,
            status='Service Boy Assigned')

        Order = []
        Assinged_Order = []

        for customer_hist in Customer_Hist.values():
            customer = Customer.objects.filter(
                customer_id=customer_hist['customer_id'])

            hospital = Hospital_Detail.objects.filter(
                hospital_id=customer_hist['hospital_id'])

            if(Active_Service_Boy['pin_serve'].find(str(hospital[0].hospital_pin)) != -1):

                Order.append({
                    'Order_ID': customer_hist['customer_trip_id'],
                    'customer': customer_hist['customer_FName'] + ' ' + customer_hist['customer_LName'],
                    'service_chosen': customer_hist['selected_service'],
                    'pickup_address': customer[0].address,
                    'drop_address': hospital[0].hospital_address,
                    'hospital_name': hospital[0].hospital_name,
                    'PIN': hospital[0].hospital_pin,
                    'price': customer_hist['amount'],
                    'order_date': customer_hist['date_of_booking'],
                    'service_date_time': customer_hist['date_of_service'],
                })

        for customer_hist in Customer_Pending_Hist.values():
            customer = Customer.objects.filter(
                customer_id=customer_hist['customer_id'])

            hospital = Hospital_Detail.objects.filter(
                hospital_id=customer_hist['hospital_id'])

            Assinged_Order.append({
                'Order_ID': customer_hist['customer_trip_id'],
                'customer': customer_hist['customer_FName'] + ' ' + customer_hist['customer_LName'],
                'service_chosen': customer_hist['selected_service'],
                'pickup_address': customer[0].address,
                'drop_address': hospital[0].hospital_address,
                'hospital_name': hospital[0].hospital_name,
                'PIN': hospital[0].hospital_pin,
                'price': customer_hist['amount'],
                'order_date': customer_hist['date_of_booking'],
                'service_date_time': customer_hist['date_of_service'],
            })
            
        request.session['date_not_yet'] = False
        if request.session['date_not_yet'] == None:
            request.session['date_not_yet'] = False
        try:
            if request.method == 'POST':
                newService = request.POST.get('newService')
                customer_service_hist = Customer_Service_Hist.objects.filter(
                    customer_trip_id=int(newService),
                    status='pending',
                )
                service_boy = Service_Boy.objects.filter(ID=ID)
                if(customer_service_hist.exists()):
                    confirm_order = customer_service_hist.values()[0]
                    hospital = Hospital_Detail.objects.filter(
                        hospital_id=confirm_order['hospital_id'])[0]
                    
                    customer_service_hist = Customer_Service_Hist.objects.filter(
                        customer_trip_id=confirm_order['customer_trip_id'],
                        customer_id=confirm_order['customer_id']
                    )
                    customer_service_hist.update(
                        service_boy_id=ID,
                        service_boy_name=service_boy[0].first_name +
                        ' '+service_boy[0].last_name,
                        status='Service Boy Assigned',
                    )
                    customer = Customer.objects.filter(
                        customer_id=confirm_order['customer_id'])[0]

                    service_boy_order = Service_Boy_Service_Hist(
                        service_boy_trip_id=confirm_order['customer_trip_id'],
                        customer_id=confirm_order['customer_id'],
                        customer_FName=customer.first_name,
                        customer_LName=customer.last_name,
                        customer_mobile=customer.mobile,
                        status='Assigned to Customer',
                        amount=confirm_order['amount'],
                        service_boy_id=ID,
                        service_boy_name=service_boy[0].first_name +
                        ' ' + service_boy[0].last_name,
                        date_of_booking=customer_service_hist[0].date_of_booking,
                        date_of_service=customer_service_hist[0].date_of_service,
                        hospital_name=customer_service_hist[0].hospital_name,
                        hospital_id=customer_service_hist[0].hospital_id,
                        selected_service=customer_service_hist[0].selected_service,
                    )

                    service_boy.update(available=False)
                    # service_chosen=Service_Chosen.objects.filter(
                    #         service_chosen_id=confirm_order['service_chosen_id']).update(status='accepted')
                    service_boy_order.save()
                    request.session['order_already_placed_status'] = False

                    return redirect('/service_boy/' + str(ID))
                else:
                    request.session['order_already_placed_status'] = True
                    return redirect('/service_boy/' + str(ID))
            return render(request, 'service_boy/service_boy_dashboard.html', {
                'Active_Service_Boy': Active_Service_Boy,
                'Order': reversed(Order),
                'Assinged_Order': reversed(Assinged_Order),
                'order_already_placed_status': request.session['order_already_placed_status'],
                'date_not_yet': request.session['date_not_yet'],
            })
        except:
            return render(request, 'service_boy/service_boy_dashboard.html', {
                'Active_Service_Boy': Active_Service_Boy,
                'Order': reversed(Order),
                'Assinged_Order': reversed(Assinged_Order),
                'date_not_yet': request.session['date_not_yet'],
            })
    except:
        return redirect('/login')

def start_ride(request, ID):
    try:
        Active_Service_Boy = request.session['Active_Service_Boy']

        if request.method == 'POST':
            request.session['date_not_yet'] = False
            if(request.POST.get('assignService', '') != ''):
                request.session['trip_ID'] = request.POST.get('assignService', '')
            sendOTP = request.POST.get('send_OTP', '')
            OTP_entered = request.POST.get('OTP_entered', '')
            stop = request.POST.get('stop', '')
            stop_customer_time = request.POST.get('stop_customer_time', '')
            # if( trip_ID != ''):
            service_boy_order = Service_Boy_Service_Hist.objects.filter(
                service_boy_trip_id=int(request.session['trip_ID'])).values()[0]
            customer_service_hist = Customer_Service_Hist.objects.filter(
                customer_trip_id=int(request.session['trip_ID'])).values()[0]
            date_of_service = date_break(service_boy_order['date_of_service'])
            date_of_service = date_of_service.strftime("%Y-%m-%d")
            now = datetime.today()
            dt_string = now.strftime("%Y-%m-%d")
            convert_services = customer_service_hist['selected_service']
            characters_to_remove = "[]'"
            for character in characters_to_remove:
                convert_services = convert_services.replace(
                    character, "")
            convert_services = convert_String_to_List(convert_services)
            if dt_string != date_of_service:
                request.session['date_not_yet'] = True
                return redirect('/service_boy/' + str(ID))
            customer = Customer.objects.filter(
                customer_id=customer_service_hist['customer_id'])[0]
            if stop_customer_time != '':
                stop_customer_id = request.POST.get('stop_customer_id', '')
                # milliseconds did timer last
                stop_customer_time = int(stop_customer_time)/(1000 * 60)
                
                ride_complete.ride_complete(request.session['trip_ID'], stop_customer_time, Customer_Service_Hist,
                                            Service_Boy_Service_Hist, Customer_Ongoing_Trip, Service_Boy_Ongoing_Trip)
                return redirect('/service_boy/' + str(ID))

            if sendOTP != '':
                request.session['once_start_ride'] = False
                request.session['otp_send'] = {
                    'otp': otp_generator(),
                    'customer': customer.customer_id,
                    'email': customer.email,
                    'mobile': customer.mobile
                }
                # mail the OTP to customer email

                send_otp_to_customer(request.session['otp_send'])

                otp_send = True

                return render(request, 'service_boy/start_ride.html', {
                    'otp_send': otp_send,
                    'Active_Service_Boy': Active_Service_Boy,
                    'trip_ID': request.session['trip_ID'],
                    'customer_service_hist': customer_service_hist,
                    'convert_services': convert_services,
                    'customer_pickUp': customer,
                    'hospital_drop': Hospital_Detail.objects.filter(hospital_id=customer_service_hist['hospital_id'])[0]
                })

            if OTP_entered != '' and request.session['once_start_ride'] == False:
                request.session['once_start_ride'] = True

                if (OTP_entered == request.session['otp_send']['otp']):
                    otp_correct = True

                    Customer_Service_Hist.objects.filter(customer_trip_id=int(request.session['trip_ID'])).update(
                        status='Service Started',
                    )

                    Service_Boy_Service_Hist.objects.filter(service_boy_trip_id=int(request.session['trip_ID'])).update(
                        status='Driving With Customer',
                    )
                    
                    Service_Boy.objects.filter(ID=service_boy_order['service_boy_id']).update(current_status='with customer')
                    service_boy_ongoing = Service_Boy_Ongoing_Trip(
                        service_boy_trip_id=service_boy_order['service_boy_trip_id'],
                        customer_id=service_boy_order['customer_id'],
                        customer_FName=service_boy_order['customer_FName'],
                        customer_LName=service_boy_order['customer_LName'],
                        customer_mobile=service_boy_order['customer_mobile'],
                        service_boy_id=service_boy_order['service_boy_id'],
                        amount=service_boy_order['amount'],
                        service_boy_name=service_boy_order['service_boy_name'],
                        date_of_booking=service_boy_order['date_of_booking'],
                        date_of_service=service_boy_order['date_of_service'],
                        hospital_name=service_boy_order['hospital_name'],
                        hospital_id=service_boy_order['hospital_id'],
                        selected_service=service_boy_order['selected_service'],
                        start_date_time=datetime.today()
                    )

                    customer_ongoing_trip = Customer_Ongoing_Trip(
                        customer_trip_id=customer_service_hist['customer_trip_id'],
                        customer_id=customer_service_hist['customer_id'],
                        customer_FName=customer_service_hist['customer_FName'],
                        customer_LName=customer_service_hist['customer_LName'],
                        customer_mobile=customer_service_hist['customer_mobile'],
                        date_of_booking=customer_service_hist['date_of_booking'],
                        date_of_service=customer_service_hist['date_of_service'],
                        amount=customer_service_hist['amount'],
                        service_boy_id=customer_service_hist['service_boy_id'],
                        service_boy_name=customer_service_hist['service_boy_name'],
                        gender=Service_Boy.objects.filter(
                            ID=customer_service_hist['service_boy_id'])[0].gender,
                        hospital_name=customer_service_hist['hospital_name'],
                        hospital_id=customer_service_hist['hospital_id'],
                        selected_service=customer_service_hist['selected_service'],
                        start_date_time=datetime.today()
                    )
                    service_boy_ongoing.save()
                    customer_ongoing_trip.save()

                else:
                    otp_correct = False

                return render(request, 'service_boy/start_ride.html', {
                    'otp_correct':  otp_correct,
                    'otp_enter': True,
                    'Active_Service_Boy': Active_Service_Boy,
                    'trip_ID': request.session['trip_ID'],
                    'customer_service_hist': customer_service_hist,
                    'convert_services': convert_services,
                    'customer_pickUp': customer,
                    'hospital_drop': Hospital_Detail.objects.filter(hospital_id=customer_service_hist['hospital_id'])[0]
                })
                
        return render(request, 'service_boy/start_ride.html', {
            'Active_Service_Boy': Active_Service_Boy,
            'trip_ID': request.session['trip_ID'],
            'customer_service_hist': customer_service_hist,
            'convert_services': convert_services,
            'customer_pickUp': customer,
            'hospital_drop': Hospital_Detail.objects.filter(hospital_id=customer_service_hist['hospital_id'])[0]
        })
    except:
        return redirect('/login')

def all_services(request, ID):
    try:
        Active_Service_Boy = request.session['Active_Service_Boy']
        Customer_Hist = Customer_Service_Hist.objects.filter(
            service_boy_id=ID)

        Order = []
        Total_Earning = 0
        for customer_hist in Customer_Hist.values():
            customer = Customer.objects.filter(
                customer_id=customer_hist['customer_id'])

            hospital = Hospital_Detail.objects.filter(
                hospital_id=customer_hist['hospital_id'])

            if(Active_Service_Boy['pin_serve'].find(str(hospital[0].hospital_pin)) != -1):

                Order.append({
                    'Order_ID': customer_hist['customer_trip_id'],
                    'customer': customer_hist['customer_FName'] + ' ' + customer_hist['customer_LName'],
                    'service_chosen': customer_hist['selected_service'],
                    'pickup_address': customer[0].address,
                    'drop_address': hospital[0].hospital_address,
                    'hospital_name': hospital[0].hospital_name,
                    'PIN': hospital[0].hospital_pin,
                    'price': customer_hist['amount'],
                    'order_date': customer_hist['date_of_booking'],
                    'service_date_time': customer_hist['date_of_service'],
                })
                Total_Earning = Total_Earning+customer_hist['amount']

        return render(request, 'service_boy/all_services.html', {
            'Active_Service_Boy': Active_Service_Boy,  
            'Order':Order,
            'Total_Earning': Total_Earning,
        })
    except:
        return redirect('/login')

def convert_String_to_List(convert_services):
    List = convert_services.split(',')

    return List


def date_break(date):

    number = date[date.find(' '):date.find(',')]
    year = date[date.find(', ')+2:date.rindex(', ')]
    month_name = date[0:date.find('.')]
    month = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }[month_name]
    return datetime(int(year), int(month), int(number))


def send_otp_to_customer(customer_detail):

    # for service_boy in service_boys:
    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.starttls()
    mail_server.login("vermakaustubh28@gmail.com", "uvbulppoaoxlwzhu")
    SUBJECT = "Riders OTP"
    TEXT = "OTP for your Ride is: " +str(customer_detail['otp'])

    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    mail_server.sendmail('&&&&&&&&&&&', customer_detail['email'], message)
