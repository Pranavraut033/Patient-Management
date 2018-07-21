from django.contrib import admin
from .models import *

pr_info = ('Personal information', {'fields': ['profile', 'first_name', 'middle_name','last_name', \
                                               'gender', 'dob','bld_grp', 'phone_number', 'email', \
                                               's_address', 'city', 'state', 'country', 'pincode']})

class CasesInLine(admin.TabularInline):
    model = Case
    extra = 1


class AppointmentCasesInLine(admin.TabularInline):
    model = Appointment
    extra = 1


class DoctorAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Login information', {'fields': ['username', 'password', 'qual', 'bio', 'speciality']}),
        pr_info,
    ]
    inlines = [AppointmentCasesInLine]
    list_display = ('name', 'phone_number', 'email', 'speciality', )


class PatientAdmin(admin.ModelAdmin):
    fieldsets = [
        pr_info,
        ('Emergency information', {'fields': ['er_cont_name', 'relation', 'emergency_contact']}),
    ]
    inlines = [CasesInLine]
    list_display = ('name', 'phone_number', 'email',)


class CaseAdmin(admin.ModelAdmin):
    list_display = ('patient', '__str__', 'reg_time', 'l_visit', 'is_closed',)


admin.site.register(Disease)
admin.site.register(Appointment)
admin.site.register(Case, CaseAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Patient, PatientAdmin)
