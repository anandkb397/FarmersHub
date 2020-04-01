from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from django.db import connection
from django.contrib import messages
from pfapp.models import Person, Fruits
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
import uuid
import json

def rfact (cr,r):
    return {i[1][0]: r[i[0]] for i in enumerate(cr.description)}

def checkuser(request):
    user_l = ""
    if request.session.has_key('usr'):
        user_l = request.session['usr']
    return user_l

def pagenotfound(request):
    page = loader.get_template("404.html")
    return HttpResponse(page.render({}, request))


def index(request):
        t = loader.get_template("index.html")
        signup_page = ''
        if 'signin' in request.POST:
            if login(request):
                messages.info(request, 'Login sucessful!')
                return HttpResponseRedirect('/dashboard/', request)
        else:
        # if 'signup' in request.POST:
        #     return HttpResponseRedirect('/signup/', request)
            f = Fruits.objects.all()
            return HttpResponse(t.render({'usr': checkuser(request), 'Fruits': f,  'signup_page': signup_page}, request))


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        pwd = request.POST['pwd']
        sql = f"SELECT * FROM pfapp_person WHERE email='{email}' AND pwd='{pwd}' LIMIT 1"
        # database connection
        c = connection.cursor()
        c.execute(sql)
        c.cursor.row_factory = rfact
        user = c.fetchone()
        c.close()
        # If user exist, then a session is created. Else
        if user:
            request.session['usr'] = {'uid': user['id'], 'email': email,'type': user['type']}
            return True
        else:
            messages.info(request, 'Invalid emailID or Password')
            return HttpResponseRedirect('/', request)



def dashboard(request):
    dashboard = loader.get_template('dashboard/index.html')
    return HttpResponse(dashboard.render({'usr': checkuser(request)}, request))


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
                    msg += "\n\nThanking you,\nregards,\n\nAdministrator,\nFarmersHub."
                    mail2snd = EmailMessage('OTP for FarmersHub registration', msg, to=(email,))
                    mail2snd.send()
                    dv = json.dumps(dv)
                    snd = True
                    request.session['ky'] = ky
                except Exception as ex:
                    print('signup mail error :', str(ex))
                    stat = "Unable to verify email address provided..please check"
    return HttpResponse(d.render({'data':dv,'snd':snd,'msg': stat, 'signup_page': signup_page}, request))

