from django.shortcuts import render,redirect
from .models import Service_Boy, Customer, Temp

import os
import math
import random
import smtplib
import datetime
# Create your views here.

def index(request):
    if request.method == 'POST':
        # service = request.POST.get('service')
        service = request.POST.get('service')
        total_price = request.POST.get('total_price')
        print(service, total_price, 'index')
        return redirect('/customer_dashboard/' + str(myid) + '/search')

    return render(request, "user/index.html")

def Login(request):
    if(request.method == 'POST'):
        if(request.POST.get('who') == 'customer'):
            email = request.POST.get('email')
            password = request.POST.get('password')
            User_Info = Customer.objects.filter(email=email,password=password)
            if User_Info.exists():
                found_email = User_Info[0].email
            else:
                return render(request, 'user/login.html', {'not_found':'No customer found with given Credentials'})

            # creating session after login
            Current_User = User_Info.values()[0]
            Current_User['created_on'] = str(User_Info.values()[0]['created_on'])

            request.session['Active_User'] = Current_User

            return redirect('customer_dashboard/'+str(Current_User['customer_id']))

        elif(request.POST.get('who') == 'service_boy'):
            ID = request.POST.get('ID')
            email = request.POST.get('email')
            password = request.POST.get('password')
            Service_Boy_Info = Service_Boy.objects.filter(ID=ID, email=email,password=password)
            if Service_Boy_Info.exists():
                if Service_Boy_Info[0].status == False:
                    return render(request, 'user/login.html', {'not_found':'Your Application is Under Process.'})    
                else:
                    pass
                print('service_boy exists')
            else:
                return render(request, 'user/login.html', {'not_found':'No service_boy found with given Credentials'})

            Current_Service_Boy = Service_Boy_Info.values()[0]
            Current_Service_Boy['created_on'] = str(Service_Boy_Info.values()[0]['created_on'])

            request.session['Active_Service_Boy'] = Current_Service_Boy
            print(request.session['Active_Service_Boy'], '********************************')
            return redirect('service_boy/'+str(Current_Service_Boy['ID']))


    return render(request, "user/login.html")

def SignUp(request):
    if (request.method == 'POST'):
        

        firstname = request.POST.get('firstname', 'name')
        lastname = request.POST.get('lastname', '')
        father_husband_name = request.POST.get('father_husband_name', '')
        gender = request.POST.get('gender', '')
        address = request.POST.get('address', '')
        city_village = request.POST.get('city_village', '')
        district = request.POST.get('district', '')
        state = request.POST.get('state', '')
        pin = request.POST.get('pin', '')

        email = request.POST.get('email', '')
        email_customer = Customer.objects.filter(email=email)
        email_service_boy = Service_Boy.objects.filter(email=email)
        if email_customer.exists() or email_service_boy.exists():
            found = 'email already exists'
            return render(request, "user/signup.html", {'found': found})

        mother_tongue = request.POST.get('mother_tongue', '')
        education = request.POST.get('education', '')
        DOB = request.POST.get('DOB', '')
        pin_serve = request.POST.get('pin_serve', '')
        languages = request.POST.get('languages', '')

        number = request.POST.get('number', '')
        number_customer = Customer.objects.filter(mobile=number)
        number_service_boy = Service_Boy.objects.filter(mobile=number)
        if number_customer.exists() or number_service_boy.exists():
            found = 'number already exists'
            return render(request, "user/signup.html", {'found': found})

        adhaar = request.POST.get('adhaar', '')
        adhaar_customer = Customer.objects.filter(Adhaar=adhaar)
        adhaar_service_boy = Service_Boy.objects.filter(adhaar=adhaar)
        if adhaar_customer.exists() or adhaar_service_boy.exists():
            found = 'adhaar number already exists'
            return render(request, "user/signup.html", {'found': found})
        
        pan = request.POST.get('pan', 0)
        pan_service_boy = Service_Boy.objects.filter(pan=pan)
        if pan_service_boy.exists():
            found = 'PAN number already exists'
            return render(request, "user/signup.html", {'found': found})
        
        Bank_Account = request.POST.get('Bank_Account', 0)
        account_service_boy = Service_Boy.objects.filter(account=Bank_Account)
        if account_service_boy.exists():
            found = 'account number already exists'
            return render(request, "user/signup.html", {'found': found})
        
        IFSC_code = request.POST.get('IFSC_code', 0)
        branch = request.POST.get('branch', 0)

        image = ''
        if len(request.FILES) != 0:
            image = request.FILES['image']
            
            temp = Temp(image=image,email=email)
            temp.save()

        password = request.POST.get('password', '')
        again_password = request.POST.get('again_password', '')
        if password != again_password:
            found = 'Password and Confirm password fields are not equal'
            return render(request, "user/signup.html", {'found': found})
        
        print(image)

        request.session['params'] = {
            'who':request.POST.get('who'),
            'firstname':firstname,
            'lastname':lastname,
            'father_husband_name':father_husband_name,
            'gender': gender,
            'address':address,
            'city_village':city_village,
            'district': district,
            'state':state,
            'pin':pin,
            'email':email,
            'mother_tongue':mother_tongue,
            'education':education,
            'DOB':DOB,
            'pin_serve':pin_serve,
            'languages': languages,
            'number':number,
            'adhaar':adhaar,
            'pan':pan,
            'Bank_Account': Bank_Account,
            'IFSC_code': IFSC_code,
            'branch':branch,
            'password':password,
        }
        who = request.POST.get('who')
        return render(request, 'user/create_new_account.html', {'who':who, 'email':email})

    return render(request, "user/signup.html")

def create_new_account(request):
    params_dict = request.session.get('params')
    if (request.method == 'POST' and request.POST.get('get_OTP')=='Get OTP'):
        email = params_dict['email']
        who = params_dict['who']
        OTP = otp_generator(email)
        request.session['OTP'] = OTP
        return render(request, 'user/create_new_account.html', {'who':who,'email':email,'sent':'an OTP has been send to '+email})

    elif(request.method == 'POST' and request.POST.get('OTP') != ''):
        success = ''
        if (request.session.get('OTP') == request.POST.get('OTP')):
            if params_dict['who'] == 'customer':
                new_customer = Customer(first_name=params_dict['firstname'], last_name=params_dict['lastname'], father_husband_name=params_dict['father_husband_name'],
                                        email=params_dict['email'], mobile=params_dict['number'], address=params_dict['address'], state=params_dict['state'], city_village=params_dict['city_village'],
                                        PIN=params_dict['pin'], Adhaar=params_dict['adhaar'], password=params_dict['password'])
                new_customer.save()
                success =  params_dict['email'] +  ' added to List.'
            elif params_dict['who'] == 'service_boy':
                
                ID = ID_generator()
                temp = Temp.objects.filter(email=params_dict['email'])
                new_service_boy = Service_Boy(ID=ID, first_name=params_dict['firstname'], last_name=params_dict['lastname'],
                                            father_husband_name=params_dict['father_husband_name'],gender=params_dict['gender'],
                                            address=params_dict['address'], city_village=params_dict['city_village'], district=params_dict['district'], state=params_dict['state'],
                                            pin=params_dict['pin'], email=params_dict['email'], mother_tongue=params_dict['mother_tongue'], education=params_dict['education'],
                                            DOB=params_dict['DOB'], pin_serve=params_dict['pin_serve'], languages=params_dict['languages'],
                                            mobile=params_dict['number'], adhaar=params_dict['adhaar'], pan=params_dict['pan'], account=params_dict['Bank_Account'],
                                            ifsc_code=params_dict['IFSC_code'], branch=params_dict['branch'], image=temp[0].image, password=params_dict['password'])
                new_service_boy.save()
                success = params_dict['email'] + ' added to List. Please wait till we verify your Details. Mail will be sent to given Email-Address.'
        else:
            return render(request,'user/create_new_account.html',{'otp_error':'please enter correct 6 digit OTP'})
        return render(request, 'user/login.html',{'success': success})
    return render(request, "user/create_new_account.html")

def forgot_password(request):

    if (request.method == 'POST' and request.POST.get('get_OTP')=='Get OTP'):
        email = request.POST.get('email')
        OTP = otp_generator(email)
        request.session['OTP'] = OTP
        return render(request, 'user/forgot_password.html',
            {'email':email,
            'sent':'an OTP has been send to '+email, 
            # 'disabled':'disabled',
            'content':'content' 
            })
    elif(request.method == 'POST' and request.POST.get('OTP') != ''):
        OTP = request.POST.get('OTP')
        email = request.POST.get('email')
        password = request.POST.get('password')
        again_password = request.POST.get('again_password')
        if(password != again_password):
            return render(request,'user/forgot_password.html',
                {'error':'password and confirm password must match',
                'email':email,
                'disabled':'disabled',
                'content':'content' 
                })
        elif(request.session.get('OTP') != OTP):
            return render(request,'user/forgot_password.html',
            {'error':'please enter correct 6 digit OTP',
            'email':email,
            'disabled':'disabled',
            'content':'content' 
            })
        else:
            print(email)
            User_Exist = Customer.objects.filter(email=email)
            Service_Boy_Exist = Service_Boy.objects.filter(email=email) 
            if (User_Exist.exists()):
                for User in User_Exist:
                    User.password = password
                    User.save()
            elif (Service_Boy_Exist.exists()):
                for User in Service_Boy_Exist:
                    User.password = password
                    User.save()
            else:
                return render(request,'user/forgot_password.html',{'error':'No User found with given E-mail'})
        return render(request, 'user/login.html',{'success':'password changed successfully'})
    return render(request, 'user/forgot_password.html')


def customer_dashboard(request):
    return render(request, 'user/customer_dashboard.html')

def otp_generator(email):
    OTP = ''
    for _ in range (6):
        random_num = random.randint(0,9)
        OTP = OTP + str(random_num)
    print(OTP)
    
    mail_server = smtplib.SMTP('smtp.gmail.com', 587)
    mail_server.starttls()
    mail_server.login("vermakaustubh28@gmail.com", "uvbulppoaoxlwzhu")
    message = "Please don't share this OTP with anyone. Your OTP is "+OTP
    mail_server.sendmail('&&&&&&&&&&&', email, message)

    return OTP

def ID_generator():
    ID = ''
    for _ in range (6):
        random_num = random.randint(0,9)
        ID = ID + str(random_num)
    if(Service_Boy.objects.filter(ID=ID).exists()):
        return ID_generator()
    else:
        return ID
