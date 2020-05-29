from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.db import connection
from django.contrib import messages
from pfapp.models import Person, Fruits, User_locations, user_details
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
import uuid
import json
from datetime import date

def rfact (cr,r):
    return {i[1][0]: r[i[0]] for i in enumerate(cr.description)}

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def checkuser(request):
    user_l = ""
    if request.session.has_key('usr'):
        user_l = request.session['usr']
    return user_l

# def pagenotfound(request):
#     page = loader.get_template("404.html")
#     return HttpResponse(page.render({}, request))


def index(request):
        signup_page = ''
        if 'signin' in request.POST:
            login(request)
        if checkuser(request):
            loged_user = request.session['usr']
            if loged_user.get('type') == 'consumer':
                return redirect('Explore/')
            else:
                return redirect('Profile/')
            # return render(request, 'dashboard_index.html', {'usr': checkuser(request), 'content_view': content_view,'user_exist':user_exist,'loged_user_type':loged_user_type})
        else:
            f = Fruits.objects.all()
            return render(request, 'index.html', {'usr': checkuser(request), 'Fruits': f, 'signup_page': signup_page})
        

def view_profile(request,email):
    if checkuser(request):
        user_exist = 0
        remail = email
        content_view = 'Explore_Farmers'
        with connection.cursor() as c:
            c.execute(f"SELECT * FROM pfapp_person JOIN pfapp_user_locations ON pfapp_user_locations.person_id = pfapp_person.id JOIN pfapp_user_details ON pfapp_user_details.person_id = pfapp_person.id WHERE pfapp_person.email='{remail}' LIMIT 1")
            c.cursor.row_factory = rfact
            q_usr = c.fetchone()
        user_exist = 1
        return render(request, 'dashboard_index.html', {'usr': checkuser(request), 'content_view': content_view,'qusr':q_usr,'user_exist':user_exist,})
    else:
        messages.info(request, 'Login Now to view this page!!!')
        return redirect('/')

def Explore(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        user_exist = 0
        content_view = 'Explore_Farmers'
        usertype = 'farmer'
        location = 'thrissur'
        with connection.cursor() as c:
            c.execute(f"SELECT * FROM pfapp_person JOIN pfapp_user_locations ON pfapp_user_locations.person_id = pfapp_person.id JOIN pfapp_user_details ON pfapp_user_details.person_id = pfapp_person.id WHERE pfapp_person.type='{usertype}' AND pfapp_user_locations.locality='{location}' ")
            farmer = dictfetchall(c)
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view,'farmers':farmer,'user_exist':user_exist}, request))
    else:
        messages.info(request, 'Login Now !')
        return redirect('/')

def Settings(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Settings'
        if 'settings_pwd_button' in request.POST:
            # password updation code here
            messages.info(request, 'Password Updated sucessfully!')
        if 'settings_location_button' in request.POST:
            # location updation code here
            messages.info(request, 'Location Updated sucessfully!')
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')

def Delivery_Conformation(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Delivery_Conformation'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')

def My_Earnings(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'My_Earnings'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!!')
        return redirect('/')

def Learn_Farming(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Learn_Farming'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Surpluse_Market(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Surpluse_Market'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def My_Farmers(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'My_Farmers'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def My_Customers(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'My_Customers'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Dispatch_Manager(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Dispatch_Manager'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Customer_Reviews(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Customer_Reviews'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def New_Request(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Contracts_Manager'
        content_view_sub = 'New_Request'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view,'content_view_sub': content_view_sub,}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Active_Contracts(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Contracts_Manager'
        content_view_sub = 'Active_Contracts'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view,'content_view_sub': content_view_sub,}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Expired_Contracts(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Contracts_Manager'
        content_view_sub = 'Expired_Contracts'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view,'content_view_sub': content_view_sub,}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Add_Contracts(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Contracts_Manager'
        content_view_sub = 'Add_Contracts'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view,'content_view_sub': content_view_sub,}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')

def Profile(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'Profile'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')


def My_Contracts(request):
    if checkuser(request):
        viewPage = loader.get_template('dashboard_index.html')
        content_view = 'My_Contracts'
        return HttpResponse(viewPage.render({'usr': checkuser(request), 'content_view': content_view}, request))
    else:
        messages.info(request, 'Login Now to view this page!')
        return redirect('/')




def login(request):
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['pwd']
        # # sql = f"SELECT * FROM pfapp_person WHERE email='{email}' AND pwd='{pwd}' LIMIT 1"
        # sql = f"SELECT * FROM pfapp_person, pfapp_user_details, pfapp_user_locations WHERE pfapp_person.email ='{email}' AND pwd='{pwd}' LIMIT 1"
        # # database connection
        # c = connection.cursor()
        # c.execute(sql)
        # c.cursor.row_factory = rfact
        # user = c.fetchone()
        # c.close()

        with connection.cursor() as c:
            c.execute(f"SELECT * FROM pfapp_person JOIN pfapp_user_locations ON pfapp_user_locations.person_id = pfapp_person.id JOIN pfapp_user_details ON pfapp_user_details.person_id = pfapp_person.id WHERE pfapp_person.email ='{email}' AND pfapp_person.pwd='{pwd}' LIMIT 1 ")
            c.cursor.row_factory = rfact
            user = c.fetchone()

        # If user exist, then a session is created.
        if user:
            request.session['usr'] = {'id': user['id'], 'email': email, 'type': user['type'],'name': user['name'], 'country': user['country'], 'locality': user['locality'], 'phoneno':user['phoneno']}
            return True
        else:
            messages.info(request, 'Invalid emailID or Password')
            return HttpResponseRedirect('/', request)

def logout(request):
    if request.session.has_key('usr'):
        del request.session['usr']
    return HttpResponseRedirect('/', request)

def signup(request):
    d = loader.get_template("signup.html")
    signup_page = 'true'
    msg = ''
    stat = ''
    dv = {}
    snd = False
    if request.method == "POST":

        if 'btncnf' in request.POST:

            if request.session.has_key('ky'):
                otp = request.POST['otp']
                data = request.POST['hdata']

                if otp == request.session['ky']:
                    dv = json.loads(data)
                    email = dv['email']
                    pwd = request.POST['pwd']
                    user_type = "consumer"

                    c = connection.cursor()
                    sql = f"INSERT INTO pfapp_person (email,pwd,type) VALUES('{email}','{pwd}','{user_type}')"
                    c.execute(sql) # so id is primary key wewill save photo as id.png ex:-1.png,2.png,in a sepafrated folder in static
                    lrowid=c.lastrowid # will return the autoincremented primary key value for the current insert
                    c.close()
                    if lrowid:
                        if 'fimg' in request.FILES:
                            fimg = request.FILES['fimg']
                            fs = FileSystemStorage()
                            fnam = 'pfapp/static/usrimg/' + str(lrowid) + '.png'
                            if fs.exists(fnam):
                                fs.delete(fnam)
                            fs.save(fnam, fimg)
                    messages.info(request, 'Account created sucessfully!')
                    return HttpResponseRedirect('/',request)
                else:
                    stat = "Invalid OTP please verify with your mail..!"
                    dv = data
                    snd = True
            else:
                stat = "Timeout..session expired..please retry..!"


        else:
            email = request.POST['email']
            dv = {'email': email}
            sql = f"SELECT * FROM pfapp_person WHERE email='{email}' LIMIT 1"
            c = connection.cursor()  # connecting the database
            c.execute(sql)
            c.cursor.row_factory = rfact
            user = c.fetchone()
            c.close()
            if user:
                stat = 'user already exist.\n'
                stat += '\nTry login instead.'
            else:
                try:
                    ky = uuid.uuid4().hex[:6].upper() # OTP created.
                    # send mail
                    msg = "Dear Customer,\nThank you for registering with FarmersHub.\n"
                    msg += f"\n\nYour OTP is :{ky} \n please provide it in the space provided in your registartion form."
                    msg += "\n\nThanking you,\nregards,\n\nAdministrator,\nFarmersHub."
                    mail2snd = EmailMessage('OTP for FarmersHub registration', msg, to=(email,), cc=(), bcc=())
                    mail2snd.send()
                    dv = json.dumps(dv)
                    snd = True
                    request.session['ky'] = ky
                except Exception as ex:
                    print('signup mail error :', str(ex))
                    stat = "Unable to verify email address provided..please check"
    return HttpResponse(d.render({'data':dv,'snd':snd,'msg': stat, 'signup_page': signup_page}, request))
