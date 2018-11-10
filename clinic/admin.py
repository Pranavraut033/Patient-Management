from django.contrib import admin
from .models import *
import nested_admin

com_info = ('Personal information', {'fields': ['profile', 'first_name', 'middle_name','last_name', \
											   'gender', 'dob','blood_type', 'email', ]})
'''
	- Clinic -
'''
class CBranchAssistantDoctorInline(nested_admin.NestedTabularInline):
	model = BranchAssistantDoctor
	extra = 2

class CBranchAddressInline(nested_admin.NestedTabularInline):
	model = BranchAddress
	extra = 1

class CBranchPhoneInline(nested_admin.NestedTabularInline):
	model = BranchPhone
	extra = 1

class CBranchTimmingInline(nested_admin.NestedTabularInline):
	model = BranchTimming
	extra = 5

class CBranchEmployeeInline(nested_admin.NestedTabularInline):
	model = BranchEmployee
	extra = 2

class CBranchInline(nested_admin.NestedStackedInline):
	model = Branch
	extra = 0
	inlines = [CBranchEmployeeInline, CBranchPhoneInline, CBranchAssistantDoctorInline, CBranchAddressInline, CBranchTimmingInline, ]

class ClinicPhoneInline(nested_admin.NestedTabularInline):
	model = ClinicPhone
	extra = 1

class ClinicAdmin(nested_admin.NestedModelAdmin):
	inlines = [ClinicPhoneInline, CBranchInline]
'''
	- end -

	- BranchAdmin -
'''
class BranchAssistantDoctorInline(admin.TabularInline):
	model = BranchAssistantDoctor

class BranchAddressInline(admin.TabularInline):
	model = BranchAddress
	extra = 1

class BranchPhoneInline(admin.TabularInline):
	model = BranchPhone
	extra = 1

class BranchTimmingInline(admin.TabularInline):
	model = BranchTimming
	extra = 5

class BranchEmployeeInline(admin.TabularInline):
	model = BranchEmployee
	extra = 3

class BranchAdmin(admin.ModelAdmin):
	inlines = [BranchAssistantDoctorInline, BranchEmployeeInline, BranchPhoneInline, BranchAddressInline, BranchTimmingInline, ]
	model = BranchEmployee
	extra = 3
'''
	- end -

	- Generic Person admin -
'''
class PersonPhoneInline(nested_admin.NestedTabularInline):
	model = PersonPhone

class PersonAddressInline(nested_admin.NestedTabularInline):
	model = PersonAddress

class EmergencyContactPhoneInline(nested_admin.NestedTabularInline):
	model = EmergencyContactPhone
	extra = 0

class EmergencyContactInline(nested_admin.NestedTabularInline):
	model = EmergencyContact
	extra = 1
	inlines = [EmergencyContactPhoneInline]

class PersonAdmin(nested_admin.NestedModelAdmin):
	inlines = [PersonAddressInline, PersonPhoneInline, EmergencyContactInline, ]
'''
	- End -

	- Others -
'''
class DoctorAdmin(PersonAdmin):
	fieldsets = [
		('Login information', {'fields': ['username', 'password',]}),
		('Extra', {'fields': ['qual', 'bio', 'speciality',]}),
		com_info,
	]
	list_display = ('username', 'full_name', 'email', 'speciality', 'reg_time')

class PatientAdmin(PersonAdmin):
	fieldsets = [
		com_info,
		('Extra', {'fields':['clinic', 'occupation','med_info']}),
	]
	list_display = ('full_name', 'email', 'reg_time')
'''
	- End -

	- Case -
'''
class VisitDrugInline(nested_admin.NestedTabularInline):
	model = VisitDrug
	extra = 0

class VisitComplaintInLine(nested_admin.NestedTabularInline):
	model = VisitComplaint
	extra = 1

class VisitExaminationInline(nested_admin.NestedTabularInline):
	model = VisitExamination
	extra = 1

class CaseVisitInline(nested_admin.NestedTabularInline):
	model = CaseVisit
	extra = 1
	inlines = [VisitDrugInline, VisitComplaintInLine, VisitExaminationInline]

class CaseDiseaseInline(nested_admin.NestedTabularInline):
	model = CaseDisease
	extra = 1

class CaseReportInline(nested_admin.NestedTabularInline):
	model = CaseReport
	extra = 0

class CaseAdmin(nested_admin.NestedModelAdmin):
	fieldsets = [
		('Details', {'fields': ['title', 'doctor', 'patient', 'date',]}),
		('Extra', {'fields': ['refer',]})
	]
	inlines = [CaseDiseaseInline, CaseReportInline, CaseVisitInline]
	list_display = ('title', 'patient', 'date')
'''
	- End -
'''
admin.site.register(Address)
admin.site.register(Phone)
admin.site.register(Disease)
admin.site.register(Drug)
admin.site.register(CaseAppointment)
admin.site.register(Case, CaseAdmin)

admin.site.register(Person, PersonAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)

admin.site.register(Branch, BranchAdmin)
admin.site.register(Clinic, ClinicAdmin)
