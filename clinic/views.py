from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from .forms import *
from .models import *
from .utils import log
from django.core.exceptions import ObjectDoesNotExist

site_url = '/'

# Create your views here.
def index(request):
    try:
        d =  Doctor.objects.get(pk=request.session['current_user'])
        context = {'doctor': d}
        # todo continue here
        return render(request, 'clinic/index.html', context)
    except (ObjectDoesNotExist, KeyError) as ex:
        err_msg = None
        if isinstance(ex, ObjectDoesNotExist):
            del request.session['current_user']
            err_msg = 'Doctor Deleted!'
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                d = Doctor.objects.filter(username=form['username'].value())
                if len(d) == 0:
                    err_msg = 'Username not found'
                else:
                    d = d[0]
                    if d.verify_password(form['password'].value()):
                        request.session['current_user'] = d.username
                        return redirect(site_url + 'clinic/')
                    else:
                        err_msg = 'Invalid password'
        else:
            form = LoginForm()
        context = {'login_form' : form, 'error_message' : err_msg}
        return render(request, 'clinic/login.html', context)

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
    return render(request, 'clinic/template_new.html', {'form' : form, 'next' : '/%s/new' % (obj), \
            'previous' : prv, 'obj' : str(form), 'error_message' : err_msg, })
