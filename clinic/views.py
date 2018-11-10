from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime as DATE
from datetime import date

from clinic.models import *
from clinic.utils import log, utilities
from clinic.forms import *

logger = log.Logger()

def get_user(request):
	return Doctor.objects.get(pk=request.session['doctor_id'])

def index(request):
	context, page = {'model_doctor' : Doctor, }, 'index.html'
	if 'doctor_id' in request.session:
		try:
			doctor = get_user(request)
			context['doctor'] = doctor
			if 'clinic_id' in request.session:
				clinic = Clinic.objects.get(pk=request.session['clinic_id'])
				context["clinic_head"] = True
				context['branch'] = clinic.branch_set.get(pk=request.session['branch_id'])
				context['branches'] = list(clinic.branch_set.all())
				context['branches'].remove(context['branch'])
			elif 'branch_id' in request.session:
				context['branch'] = Branch.objects.get(pk=request.session['branch_id'])
		except (ObjectDoesNotExist) as ex:
			logger.w(ex)
			return logout(request)
	else:
		page = "login.html"
		if request.method == 'POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				username = request.POST['username']
				d = Doctor.objects.get(pk=username)
				try:
					clinic = d.clinic
					request.session['clinic_id'] = clinic.pk
					try:
						request.session['branch_id'] = d.branch.pk
					except ObjectDoesNotExist as e:
 						request.session['branch_id'] = clinic.branch_set.all()[0].pk
				except ObjectDoesNotExist as ex:
					try:
						request.session['branch_id'] = d.branch.pk
					except ObjectDoesNotExist as e:
						try:
							request.session['branch_id'] = d.branchassistantdoctor.branch.pk
						except Exception as e:
							# TODO: add_cookie to show error
							context['ermsg'] = "Username '" + username + "' doesn't have branch associated with it contact Database administrative"
							logger.w(e, "Username '" + username + "' doesn't have branch associated with it contact Database administrative")
							return render(request, 'clinic/' + page, context)
				request.session['doctor_id'] = username
				return redirect('/clinic')
			else:
				context['extra'] = {'values' : form.data , 'errors' : dict(form.errors)}
	return render(request, 'clinic/' + page, context)

def logout(request):
	try:
		del request.session['doctor_id']
	except KeyError: pass
	return redirect('/clinic')

def add_patient(request):
	d, clinic = None, None
	try:
		d = get_user(request)
		if 'clinic_id' in request.session:
			clinic = Clinic.objects.get(pk=request.session['clinic_id'])
		elif 'branch_id' in request.session:
			clinic = branch.objects.get(pk=request.session['branch_id']).clinic
		else: clinic = d.branchassistantdoctor.branch.clinic
	except Exception as e:
		logger.e(e, "views.py > add_patinet: Getting Patient Failed");
		raise e
		# return logout(request)
	form = PatientFormSet(request.POST, clinic)
	context = {'doctor' : d, "form" : form.get_form_as_table(), }

	if request.method == "POST":
		if form.is_valid:
			p = form.save()
		else:
			context['extra'] = {'data' : None, 'errors' : dict(forms.get_errors()), }
	else:
		pass
	return render(request, 'clinic/new-patient.html', context)

add_functions = {
	'patient' : add_patient
}

def add(request, model):
	return add_functions[model](request)

# models = {'doctor' : Doctor,
# 		  'patient' : Patient,
# 		  'case' : Case,
# 		  'appt' : CaseAppointment, }

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
# 	form = DoctorForm()
# 	if request.method == 'POST':
# 		form = DoctorForm(request.POST)
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
# 		form = PatientForm(request.POST)
# 		if form.is_valid():
# 			try:
# 				patient = form.save(context['doctor_id'])
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
