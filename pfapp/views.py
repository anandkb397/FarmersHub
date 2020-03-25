from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.db import connection
from django.contrib import messages
from pfapp.models import Person, Fruits
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from .admin import Person
from django.contrib.auth import authenticate, login, logout
import uuid
import json

def rfact (cr,r):
    return {i[1][0]:r[i[0]] for i in enumerate(cr.description)}

def index(request):
    # try:
        t= loader.get_template("index.html")
        #code for login
        nousr = True
        wrong_pwd = False

        #codes for signin and signup
        if request.method == "POST":
            #code to signin
            if 'signin' in request.POST:
                # email = request.POST['email']
                # pwd = request.POST['pwd']
                user = authenticate(request, email=request.POST['email'], password=request.POST['pwd'])
                if user is not None:
                    login(request, user)
                    nousr = False
                    messages.info(request, 'Login sucessful!')
                    # request.session['email'] = email
                    return HttpResponseRedirect('/dashboard/', request)
                else:
                    messages.info(request, 'Invalid Email Id or Password!')
            # code to signup
            if 'signup' in request.POST:
                signup_user = authenticate(request, email=request.POST['email'], password=request.POST['pwd'])
                if signup_user is not None:
                    messages.info(request, 'User Exists!')
                else:
                    signup_user = User.objects.create_user(username=request.POST['email'], email=request.POST['email'], password=request.POST['pwd'])
                    messages.info(request, 'user Created')
                    messages.info(request, 'Login Now')
                    return HttpResponseRedirect('/', request)

        ##code for displaying  fruits list under products
        f = Fruits.objects.all()
        return HttpResponse(t.render({'nousr': nousr, 'wrong_pwd': wrong_pwd, 'Fruits': f}, request))
    # except Exception as ex:
    #     return HttpResponseRedirect('/404/', request)




def dashboard(request):
    try:
        dashboard = loader.get_template('dashboard.html')
        return HttpResponse(dashboard.render({}, request))
    except Exception as ex:
        return HttpResponseRedirect('', request)



def logout_view(request):
    logout(request)
    return HttpResponseRedirect('', request)
    # Redirect to a success page.

def signin(request):
    d = loader.get_template("login.html")
    stat = ''
    nousr = True
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['pwd']
        lk = Person(email=email, pwd=pwd)
        try:
            if lk.email == email & lk.pwd == pwd:
                request.session['email'] = lk.email
                return HttpResponseRedirect('/', request)
            else:
                nousr = False
        except Exception as ex:
            stat = "Unable to verify email address provided..please check"
    return HttpResponse(d.render({'nousr': nousr, 'stat': stat}, request))

def checkuser(request):
    user_l = ""
    if request.session.has_key('usr'):
        user_l = request.session['usr']
    return user_l

def logout(request):
    if request.session.has_key('usr'):
        del request.session['usr']
    return HttpResponseRedirect('/', request)

#from django.core.files.storage import FileSystemStorage
def signup(request):
    d = loader.get_template("signup.html")
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

                    c = connection.cursor()
                    sql = f"INSERT INTO pfapp_person (email,pwd,type) VALUES('{email}','{pwd}','farmer')"
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
                    stat = 'sucessfully created account'
                    #del request.session[dv['email']]
                    return HttpResponseRedirect('/login/',request)
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
                # msg = 'user already exist'
                # return HttpResponseRedirect('/login/', request)
                stat = 'user already exist'
                #del request.session['email']
                #messages.info(request, 'user already exist')
            else:
                # c = connection.cursor()
                # sql = f"INSERT INTO logintab (email,pwd) VALUES('{email}','{pwd}')"
                # c.execute(sql)
                # msg = 'successfully created account'
                # c.close()
                # messages.info(request, 'Account created sucessfully!')
                try:
                    ky = uuid.uuid4().hex[:6].upper()
                    # send mail
                    msg = "Dear Customer,\nThank you for registering with FarmersHub.\n"
                    msg += f"\n\nYour OTP is :{ky} \n please provide it in the space provided in your registartion form."
                    msg += "\n\nThanking you,\nregards,\n\nAdministrator,\nrentIT."
                    mail2snd = EmailMessage('OTP for rentIT registration', msg, to=(email,))
                    mail2snd.send()
                    dv = json.dumps(dv)
                    snd = True
                    request.session['ky'] = ky
                except Exception as ex:
                    print('signup mail error :', str(ex))
                    stat = "Unable to verify email address provided..please check"
    return HttpResponse(d.render({'data':dv,'snd':snd,'msg': stat}, request))



# def login(request):
#     lin = loader.get_template("login.html")
#     msg = ''
#     nousr = False
#     if request.method == "POST":
#         email = request.POST['email']
#         pwd = request.POST['pwd']
#         sql = f"SELECT * FROM pfapp_person WHERE email='{email}' AND pwd='{pwd}' LIMIT 1"
#
#         c = connection.cursor()
#         c.execute(sql)
#         c.cursor.row_factory = rfact
#         user = c.fetchone()
#         c.close()
#
#         if user:
#             request.session['usr'] = {'uid':user['id'],'email':email,'type':user['type']}
#             messages.info(request, 'Login sucessful!')
#             return HttpResponseRedirect('/', request)
#         else:
#             nousr = True
#     return HttpResponse(lin.render({'nousr': nousr}, request))

import http.client

def sms(request):
    lin = loader.get_template("login_old.html")
    conn = http.client.HTTPSConnection("twilio-sms.p.rapidapi.com")

    headers = {
        'x-rapidapi-host': "twilio-sms.p.rapidapi.com",
        'x-rapidapi-key': "f5977f6ce8msh6af4ce993b0ed6cp19c33ejsndb9ca0b18c33"
    }

    conn.request("GET", "/2010-04-01/Account", headers=headers)

    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return HttpResponse(lin.render({'data': data.decode("utf-8")}, request))


def pagenotfound(request):
    page = loader.get_template("404.html")
    return HttpResponse(page.render({}, request))