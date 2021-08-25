from django.shortcuts import render, redirect
from .models import Package, Service, Service_Chosen, Deals_and_Offer
from user.models import Customer, Service_Boy
from hospital.models import Hospital_Detail
from admin_control.models import Admin_Control, Customer_Service_Hist
import time
from . import message

from datetime import datetime
import random
# Create your views here.


def index(request):
    return render(request, "service/index.html")


def service_boy_on_way(request, myid):
    package_count = Package.objects.count()
    package_dict = covnert_Set_to_dict(package_count)

    customer_exist = ''
    start_time = time.time()
    Active_Service = request.session.get('Active_Service')
    print(Active_Service)
    customer = Customer.objects.filter(
        customer_id=Active_Service['customer_id'])[0]
    dt_string = ''
    try:
        if request.method == 'POST':
            if request.POST.get('pendingOrder') == 'yes':
                Service_Chosen.objects.filter(
                    service_chosen_id=Active_Service['service_id']).update(status='In Cart')

                return redirect('/customer_dashboard/'+str(Active_Service['customer_id'])+'/search')

            c = 0
            service_date_time = convert_date_and_time(
                request.POST.get('service_date_time'))[0]
            # OTP = otp_generator()

            while len(customer_exist) == 0:
                if(time.time()-start_time < 1.1):
                    time.sleep(1)
                if(time.time()-start_time < 60.1):
                    hospital = Hospital_Detail.objects.filter(
                        hospital_id=int(Active_Service['hospital_id']))[0]

                    now = datetime.now()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    request.session['No_Service_Boy'] = False

                    if c == 0:

                        Customer_Order = Customer_Service_Hist(
                            customer_trip_id=100000+Customer_Service_Hist.objects.count(),
                            customer_id=customer.customer_id,
                            customer_FName=customer.first_name,
                            customer_LName=customer.last_name,
                            customer_mobile=customer.mobile,
                            date_of_service=service_date_time,
                            amount=Active_Service['price'],
                            hospital_name=hospital.hospital_name,
                            status='pending',
                            hospital_id=hospital.hospital_id,
                            selected_service=Active_Service['service_list'],
                        )

                        Customer_Order.save()
                        
                        service_boys_available = Service_Boy.objects.filter(
                            pin_serve__contains=hospital.hospital_pin)
                        # message.send_message_to_available_service_boy(service_boys_available, Customer_Order)

                        request.session['Active_Service']['active_order_ID'] = Customer_Order.customer_trip_id
                        print(Customer_Order)
                        c = 1

                    customer_exist = Customer_Service_Hist.objects.filter(
                        customer_trip_id=Customer_Order.customer_trip_id, customer_id=myid, status='Service Boy Assigned')

                    if customer_exist.exists():
                        service_boy = Service_Boy.objects.filter(
                            ID=customer_exist[0].service_boy_id)
                        request.session['Your_Order']['service_boy_id'] = customer_exist[0].service_boy_id
                        request.session['Your_Order']['service_boy_name'] = customer_exist[0].service_boy_name
                        request.session['Your_Order']['mobile'] = service_boy[0].mobile

                        Service_Chosen.objects.filter(
                            service_chosen_id=Active_Service['service_id']).update(status='ongoing')
                        return redirect('/customer_dashboard/'+str(Active_Service['customer_id'])+'/service_boy_on_way')

                    request.session['Your_Order'] = {
                        # 'customer': customer,
                        'customer_id': Active_Service['customer_id'],
                        'service_boy_id': '',
                        'service_boy_name': '',
                        'service_boy_mobile': '',
                        'service_chosen': Active_Service['service_id'],
                        'Order_ID': Customer_Order.customer_trip_id,
                        'from': customer.address,
                        'to': hospital.hospital_address,
                        'hospital_name': hospital.hospital_name,
                        'otp': 'not active',
                        'dt_string': dt_string,
                        'price': Active_Service['price'],
                        'PIN': hospital.hospital_pin,
                    }

                else:
                    request.session['No_Service_Boy'] = True
                    return redirect('/customer_dashboard/'+str(Active_Service['customer_id'])+'/service_boy_on_way')

                    break
        cart = Cart(customer)
        print()
        print()
        print(request.session.get('Your_Order'))
        print()
        print()
        return render(request, 'service/service_boy_on_way.html', {
            'Active_Service': Active_Service,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'dt_string': dt_string,
            'Your_Order': request.session.get('Your_Order'),
            'Active_User': request.session.get('Active_User'),
            'hospital': Hospital_Detail.objects.all(),
            'hospital_city_wise': Hospital_Detail.objects.filter(hospital_city=customer.city_village),
            'cart': cart[0],
            'cart_length': cart[1],
            'No_Service_Boy': request.session['No_Service_Boy'],
            'package_dict': package_dict,
        })
    except:
        request.session['wrong'] = True
        return redirect('/customer_dashboard/'+str(Active_Service['customer_id']))


def order_confirm(request, myid):
    now = datetime.now()
    current_date_time = now.strftime("%Y-%m-%dT%H:%M")
    print(current_date_time, '2018-06-07T00:00')

    package_count = Package.objects.count()
    package_dict = covnert_Set_to_dict(package_count)
    Active_Service = request.session.get('Active_Service')
    offer_success = ''
    offer_failure = ''
    coupon = Active_Service['coupon']
    offer_amount = Active_Service['offer_amount']
    customer = Customer.objects.filter(customer_id=myid)[0]
    if request.method == 'POST':
        coupon = request.POST.get('coupon', '')
        hospital_id = request.POST.get('hospital_id', '')
        cart_value_id = request.POST.get('cart_value_id', '')

        if coupon != '' and request.session.get('Active_Service')['coupon'] == '':
            coupon_exist = Deals_and_Offer.objects.filter(offer_code=coupon)
            if coupon_exist.exists():
                price = int(request.session.get('Active_Service')['price'])
                offer_amount = (coupon_exist[0].offer_amount) / 100 * price
                price = price - offer_amount
                request.session['Active_Service']['coupon'] = coupon
                request.session['Active_Service']['price'] = round(price)
                request.session['Active_Service']['offer_amount'] = round(
                    offer_amount)
                offer_success = 'Coupon Applied'
                Service_Chosen.objects.filter(service_chosen_id=request.session['Active_Service']['service_id']).update(
                    coupon=coupon, price=round(price), service_offer_amount=offer_amount)
                # print(request.session.get('Active_Service'), 'coupon')
            else:
                offer_failure = 'Coupon Is Not Valid'

        elif hospital_id != '':
            # print(hospital_id)
            request.session['Active_Service']['hospital_id'] = hospital_id
            request.session['Active_Service']['hopital_name'] = Hospital_Detail.objects.filter(
                hospital_id=hospital_id)[0].hospital_name
            # print(Hospital_Detail.objects.filter(hospital_id=hospital_id)[0].hospital_name)

            customer_chosen = Customer.objects.filter(
                customer_id=Active_Service['customer_id'])[0]

            Order = Service_Chosen(customer_chosen=customer_chosen, service_list=Active_Service['service_list'],
                                   total_price=Active_Service['total_price'], hospital_name=request.session.get(
                'Active_Service')['hopital_name'], price=Active_Service['price'],
                coupon=Active_Service['coupon'], hospital_id=Active_Service['hospital_id'])
            Order.save()
            request.session['Active_Service']['service_id'] = Order.service_chosen_id

        elif cart_value_id != '':
            current_cart = Service_Chosen.objects.filter(
                service_chosen_id=cart_value_id)[0]

            current_cart.service_list = current_cart.service_list
            current_cart.total_price = current_cart.total_price
            characters_to_remove = "[]'"

            for character in characters_to_remove:
                current_cart.service_list = current_cart.service_list.replace(
                    character, "")
                current_cart.total_price = current_cart.total_price.replace(
                    character, "")

            Create_Session(request,
                           current_cart.service_chosen_id,
                           convert_String_to_List(current_cart.service_list),
                           convert_String_to_List(current_cart.total_price),
                           myid,
                           current_cart.hospital_id,
                           ''
                           )
            total_price = request.session.get('Active_Service')['total_price']

            Service_Chosen.objects.filter(service_chosen_id=cart_value_id).update(
                coupon='', price=total_price[len(total_price)-1], service_offer_amount=0)

        return redirect('/customer_dashboard/'+str(Active_Service['customer_id'])+'/order_confirm')
    # print(request.session.get('Active_Service'), 'id')

    selected_hospital = Hospital_Detail.objects.filter(
        hospital_id=request.session.get('Active_Service')['hospital_id'])[0]
    cart = Cart(Customer.objects.filter(
        customer_id=Active_Service['customer_id'])[0])

    return render(request, 'service/order_confirm.html', {
        'Active_Service': Active_Service,
        'Active_User': request.session.get('Active_User'),
        'selected_hospital': selected_hospital,
        'coupon': coupon,
        'offer_success': offer_success,
        'offer_failure': offer_failure,
        'offer_amount': offer_amount,
        'hospital': Hospital_Detail.objects.all(),
        'hospital_city_wise': Hospital_Detail.objects.filter(hospital_city=customer.city_village),
        'cart': cart[0],
        'cart_length': cart[1],
        'current_date_time': current_date_time,
        'package_dict': package_dict,
    })


def search(request, myid):

    package_count = Package.objects.count()
    package_dict = covnert_Set_to_dict(package_count)
    Active_User = request.session.get('Active_User')
    Active_Service = request.session.get('Active_Service')
    cart = Cart(Customer.objects.filter(
        customer_id=Active_Service['customer_id'])[0])

    customer_chosen = Customer.objects.filter(customer_id=myid)
    if 'customer_id' in Active_User:
        if(Active_User['customer_id'] == myid):
            customer_chosen = Customer.objects.filter(customer_id=myid)
            suggest_place = ''
            no_suggestion = ''
            hospital_available = ''
            hospital_pin = Active_User['PIN']
            id_pin = ''
            id_place = 'no-display'
            no_hospital = ''
            if request.method == 'POST':
                service_list = request.POST.get('service', '')
                total_price = request.POST.get('total_price', '')
                hospital_id = request.POST.get('hospital_id', '')
                search_by_place = request.POST.get('search_by_place', '')
                search_by_pin = request.POST.get(
                    'search_by_pin', Active_User['PIN'])
                hospital_available = Hospital_Detail.objects.filter(
                    hospital_pin=hospital_pin)
                if service_list != '':
                    try:
                        Create_Session(request, '', convert_String_to_List(
                            service_list), convert_String_to_List(total_price), myid, '', '')
                    except:
                        return redirect('/customer_dashboard/'+str(myid))

                elif hospital_id != '':
                    request.session['Active_Service'][
                        'hospital_id'] = hospital_id
                    Active_Service = request.session.get('Active_Service')

                    request.session['Active_Service']['service_id'] = Order.service_chosen_id
                    cart = Cart(Customer.objects.filter(
                        customer_id=Active_Service['customer_id'])[0])

                    return render(request, 'service/order_confirm.html', {
                        'Active_Service': request.session.get('Active_Service'),
                        'Active_User': request.session.get('Active_User'),
                        'selected_hospital': Hospital_Detail.objects.filter(
                            hospital_id=request.session.get('Active_Service')['hospital_id'])[0],
                        'cart': cart[0],
                        'package_dict': package_dict,
                        'cart_length': cart[1],
                        'hospital': Hospital_Detail.objects.all(),
                        'hospital_city_wise': Hospital_Detail.objects.filter(hospital_city=customer_chosen[0].city_village),
                    })

                elif search_by_place != '':
                    hospital_available = Hospital_Detail.objects.filter(
                        hospital_name__contains=search_by_place)
                    search_by_pin = ''

                    try:
                        hospital_pin = hospital_available[0].hospital_pin
                        # print('error')
                        suggest_place = Hospital_Detail.objects.filter(hospital_pin=hospital_pin).exclude(
                            hospital_name=hospital_available[0].hospital_name)
                        id_place = 'display'
                        id_pin = 'no-display'
                        if len(suggest_place) == 0:
                            no_suggestion = 'Sorry, No suggested Hospital Near by.'
                    except:
                        no_hospital = 'Sorry!, No Hospital Found with this Name.'
                        id_place = 'no-display'
                    # print(hospital_available, 'workggin')

                elif search_by_pin != '':
                    hospital_available = Hospital_Detail.objects.filter(
                        hospital_pin=search_by_pin)
                    hospital_pin = search_by_pin
                    id_pin = 'display'
                    id_place = 'no-display'
                    search_by_place = ''
                    if len(hospital_available) == 0:
                        no_hospital = 'sorry!, No Hospital Found for this location.'

            service_boys_available = Service_Boy.objects.filter(
                pin_serve__contains=hospital_pin, status=True, available=True)

            # print(Active_User['PIN'])
            try:
                return render(request, "service/search.html", {
                    'Active_User': request.session.get('Active_User'),
                    'Active_Service': request.session.get('Active_Service'),
                    'service_boys_available': service_boys_available,
                    'hospital_available': hospital_available,
                    'search_by_place': search_by_place,
                    'search_by_pin': search_by_pin,
                    'suggest_place': suggest_place,
                    'no_suggestion': no_suggestion,
                    'id_pin': id_pin,
                    'id_place': id_place,
                    'no_hospital': no_hospital,
                    'cart': cart[0],
                    'cart_length': cart[1],
                    'package_dict': package_dict,
                    'hospital': Hospital_Detail.objects.all(),
                    'hospital_city_wise': Hospital_Detail.objects.filter(hospital_city=customer_chosen[0].city_village),
                })
            except:
                print('except2')
                return redirect('/customer_dashboard/'+str(myid))
        else:
            return redirect('users:Login')
    else:
        return redirect('users:Login')

    return render(request, 'service/search.html', {
        'package_dict': package_dict,
        'hospital': Hospital_Detail.objects.all(),
        'hospital_city_wise': Hospital_Detail.objects.filter(hospital_city=customer.city_village),
        'cart': cart[0],
        'cart_length': cart[1],
    })


def customer_dashboard(request, myid):
    # print( request.session['wrong'])
    package_count = Package.objects.count()
    package_dict = covnert_Set_to_dict(package_count)
    request.session['Services'] = package_dict

    Active_Service = request.session.get('Active_Service')

    Active_User = request.session.get('Active_User')

    if Active_User['customer_id'] != Active_Service['customer_id']:
        Create_Session(request, '', [], ['0'], myid, '', '')

    cart = Cart(Customer.objects.filter(
        customer_id=Active_Service['customer_id'])[0])
    customer = Customer.objects.filter(
        customer_id=Active_Service['customer_id'])[0]
    if 'customer_id' in Active_User:
        if(Active_User['customer_id'] == myid):
            return render(request, "service/customer_dashboard.html", {
                'Active_User': request.session.get('Active_User'),
                'package_dict': package_dict,
                'hospital': Hospital_Detail.objects.all(),
                'hospital_city_wise': Hospital_Detail.objects.filter(hospital_city=customer.city_village),
                'cart': cart[0],
                'cart_length': cart[1],
            })
        else:
            return redirect('users:Login')
    else:
        return redirect('users:Login')
    return render(request, 'service/customer_dashboard.html', {
        # 'wrong': request.session['wrong'],
        'package_dict': package_dict,
        'hospital': Hospital_Detail.objects.all(),
        'hospital_city_wise': Hospital_Detail.objects.filter(hospital_city=customer.city_village),
    })


def Logout(request):
    if request.method == 'POST':
        # exiting the session
        request.session['Active_User'] = {}
        # print(request.session.get('Active_User'))
        return redirect('users:index')


def covnert_Set_to_dict(package_count):
    package_dict = []
    for package_index in range(package_count):
        # print(package_index)
        service = Service.objects.filter(package=package_index+1)
        service_list = []
        for serv in list(service.values()):
            del serv['service_addition_date']
            # del serv['package_id']
            service_list.append(list(serv.values()))
            # print(service_list)
        if(len(service_list) != 0):
            package_dict.append(service_list)
    # print(package_dict)

    return package_dict


def convert_String_to_List(service_list):
    List = service_list.split(',')
    # print(type(List), type(service_list))
    return List


def Cart(customer_chosen):
    cart_model = Service_Chosen.objects.filter(
        customer_chosen=customer_chosen, status='In Cart')
    customer_cart = []
    for item in cart_model:
        customer_cart.append(item)

    return [customer_cart, len(customer_cart)]


def Create_Session(request, service_chosen_id, service_list, total_price, myid, hospital_id, service_boy_id):

    request.session['Active_Service'] = {
        'service_id': service_chosen_id,
        'service_list': service_list,
        'total_price': total_price,
        'customer_id': myid,
        'hospital_id': hospital_id,
        'hospital_name': '',
        'service_boy_id': '',
        'offer_amount': 0,
        'price': total_price[len(total_price)-1],
        'coupon': '',
        'total_items': len(service_list),
    }


def otp_generator():
    OTP = ''
    for _ in range(4):
        random_num = random.randint(0, 9)
        OTP = OTP + str(random_num)
    print(OTP)

    return OTP


def convert_date_and_time(date_time):
    # 2021-08-14T14:02
    # Aug. 14, 2021, 2:02 p.m.

    time = date_time[date_time.find('T')+1:]

    date = date_time[0:date_time.find('T')]
    number = date[date.rindex('-')+1:]
    month = date[date_time.find('-')+1:date.rindex('-')]
    datetime_object = datetime.strptime(month, "%m")

    monthStr = datetime_object.strftime("%b")
    year = date[0:date_time.find('-')]
    # 2021-08-14
    convert_date_time = monthStr + '. ' + number + ', ' + year + ', ' + time
    list = [convert_date_time, number, month, year]
    return list
