from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .forms import *
from .models import *
from .utils import log, utilities
from django.core.exceptions import ObjectDoesNotExist
from datetime import date
site_url = '/'

def index(request): 
    context = dict()
    pg = ''
    try:
        d =  Doctor.objects.get(pk=request.session['current_user'])
        context = {'doctor': d}
        # TODO: Index Page
        pg = 'index.html'
    except (ObjectDoesNotExist, KeyError) as ex:
        # Login Page
        p_msg, u_msg = None, None
        if isinstance(ex, ObjectDoesNotExist):
            del request.session['current_user']
            err_msg = 'Doctor Deleted!'
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                d = Doctor.objects.filter(username=form['username'].value())
                if len(d) == 0:
                    u_msg = 'Username not found'
                else:
                    d = d[0]
                    if d.verify_password(form['password'].value()):
                        request.session['current_user'] = d.username
                        return redirect(site_url + 'clinic/')
                    else:
                        p_msg = 'Invalid password'
        else:
            form = LoginForm()
        context = {'login_form' : form, 'p_error' : p_msg, 'u_error' : u_msg}
        pg = 'login.html'
    return render(request, '%s' % (pg), context)

def logout(request):
    try:
        del request.session['current_user']
    except KeyError:
        pass
    return redirect(site_url + 'clinic/')


def view_obj(request, obj, pk):
    cls=eval(obj)
    obj = get_object_or_404(cls, pk=pk)
    print(obj)
    raise Http404

form_classes = {'doctor' : DoctorForm, 'patient': PatientForm,
                'case' : CaseForm, 'appt' : ApptForm}

def new_obj(request, obj):
    if obj in form_classes.keys():
        return new_human(request, obj)
    raise Http404

def new_human(request, obj):
    form_class = form_classes[obj]
    err_msg = None
    try :
        prv = request.META['HTTP_REFERER']
        if prv not in request.get_full_path():
            prv = site_url + 'clinic/'
    except KeyError:
        log.i("NO previous page found considering \"home page\"")
        prv = site_url + 'clinic/'

    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            obj, err_msg = form.save(False);
            print(obj,err_msg)
            if obj is not None:
                obj.save()
                return redirect(prv)
    else:
        form = form_class()
    
    d = utilities.get_adv_date(0, -18).__format__('20%y-%m-%d')
    return render(request, 'new-' + str(obj) +'.html', {'form' : form, 'next' : '/%s/new' % (obj), \
            'previous' : prv, 'obj' : eval(str(form)), 'error_message' : err_msg, 'time_18' : d})
