from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime as DATE
from datetime import date

from clinic.models import *
from clinic.utils import log, utilities
import clinic.forms as f

logger = log.Logger()

def login_main(request):
	context, errors = dict(), dict()
	form = f.LoginForm();

	if request.method == 'POST':
		form = f.LoginForm(request.POST)
		if form.is_valid():
			d = Doctor.objects.get(pk=form['username'].value())
			# Checking Password
			if d.verify_password(form['password'].value()):
				request.session['user'] = d.username
				return redirect('clinic/')
			else:
				errors['password'] = 'Invalid password'
		else:
			context = {'extra' : {'values' : form.data , 'errors' : dict(form.errors)}}
	elif 'error' in request.COOKIES:
		context['ermsg'] = request.COOKIES['error']
		request.session['user'] = None

	context['object'] = Doctor
	r = render(request, 'clinic/login.html', context)
	if('error' in request.COOKIES): r.delete_cookie('error')
	return r

#
# models = {'doctor' : Doctor,
# 		  'patient' : Patient,
# 		  'case' : Case,
# 		  'appt' : CaseAppointment, }
# def get_user(request):
# 	try:
# 		return Doctor.objects.get(pk=request.session['user'])
# 	except (ObjectDoesNotExist, KeyError) as ex:
# 		return ex
#

#
#
# def index(request):
# 	d = get_user(request)
# 	logger.d(type(d))
# 	if(isinstance(d, Exception)):
# 		err = 'Session Experied!'
# 		if(isinstance(d, ObjectDoesNotExist)):
# 			err = 'Login Required'
# 		response = redirect('login/');
# 		response.set_cookie('error', err, 5)
# 		return response
# 	return render(request, 'clinic/index.html', {'doctor': d})
#
#
# def logout(request):
# 	try:
# 		del request.session['current_user']
# 	except KeyError: pass
# 	return redirect(site_url + 'clinic/')
#
# # def view_object(request, object, pk):
# #     objects = []
# #     try:
# #         doctor = Doctor.objects.get(pk=request.session['current_user'])
# #         context = {'doctor' : doctor, 'pk' : pk, 'obj' : object, }
# #     except Exception as e:
# #         return redirect('/clinic/')
# #     if not object in models.keys():
# #         raise Http404
# #     model = models[object]
# #     if pk == 'all':
# #         objects = list(getattr(doctor, object + '_set').all());
# #     else:
# #         object = get_object_or_404(model, pk=int(pk))
# #         objects.append(object)
# #     context['objects'] = objects
# #     return render(request, 'clinic/view.html', context)
#
# def add_doctor(request):
# 	context = dict()
# 	form = f.DoctorForm()
# 	if request.method == 'POST':
# 		form = f.DoctorForm(request.POST)
# 		logger.d.d('Post Data:\n', request.POST)
# 		if form.is_valid():
# 			try:
# 				doctor = form.save()
# 			except Exception as e:
# 				context['extra'] = { 'errors': e.data, 'values' : form.data, }
# 			else:
# 				return redirect('/clinic/')
# 		else:
# 			context['extra'] = {'errors' : dict(form.errors), 'form' : form, 'values' : form.data, }
# 	context['object'] = Doctor
# 	context['address'] = Address
# 	return render(request, 'clinic/new-doctor.html', context)
#
# def add_patient(request):
# 	try:
# 		context = {'doctor' :  Doctor.objects.get(pk=request.session['current_user']) }
# 	except Exception as e:
# 		return redirect('/clinic/')
# 	if request.method == 'POST':
# 		form = f.PatientForm(request.POST)
# 		if form.is_valid():
# 			try:
# 				patient = form.save(context['doctor'])
# 			except Exception as e:
# 				context['extra'] = {'errors': e.data, 'values' : form.data, }
# 			else:
# 				# TODO: add success msg
# 				return redirect('/clinic/')
# 		else:
# 			context['extra'] = {'errors': dict(form.errors), 'form' : form, 'values' : form.data, }
# 	context['object'] = Patient
#
# 	return render(request, 'clinic/new-patient.html', context)
#
# def add_case(request):
# 	p = validate_user(request)
# 	if(p is not None):
# 		return p
#
# create_func = {'doctor' : add_doctor, 'patient': add_patient,
# 				'case' : add_case, }
#
# def add_object(request, object):
# 	if object in create_func.keys():
# 		return create_func[object](request)
# 	raise Http404
# #
# #
# # def handler404(request, *args, **argv):
# #     response = render_to_response('404.html', {}, context_instance=RequestContext(request))
# #     response.status_code = 404
# #     return response
