from pfapp.models import Person
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader

from django.contrib import messages


def signin(request):
    d = loader.get_template("base.html")
    nousr = True
    wrong_pwd = False
    if request.method == "POST":
        # email = request.POST['email']
        # pwd = request.POST['pwd']
        try:
            lk = Person.objects.get(email=request.POST['email'])
            if lk:
                try:
                    pk = Person.objects.get(pwd=request.POST['pwd'])
                    if pk:
                        request.session['email'] = lk.email
                        return HttpResponseRedirect('/', request)
                except Exception as ex:
                    wrong_pwd = True
        except Exception as ex:
            nousr = True
    return HttpResponse(d.render({'nousr': nousr, 'wrong_pwd': wrong_pwd}, request))

# def signin(request):
#     d = loader.get_template("login.html")
#     incorrect_details = False
#     m = Person.objects.get(email = request.POST['email'])
#     if m.pwd == request.POST['pwd']:
#         request.session['id'] = m.id
#         return HttpResponseRedirect('/',request)
#     else:
#         incorrect_details = True
#         return HttpResponse(d.render({'inc_d': incorrect_details}, request))

# def logout(request):
#     try:
#         del request.session['email']
#     except KeyError:
#         pass
#     return HttpResponse("You're logged out.")
