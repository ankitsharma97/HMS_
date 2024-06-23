from django.contrib import admin
from .models import Doctor, Patient, Status, Appointment, Report, Feedback, TreatmentPlan, History,WoundHealing

admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Status)
admin.site.register(Appointment)
admin.site.register(Report)
admin.site.register(Feedback)
admin.site.register(TreatmentPlan)
admin.site.register(History)
admin.site.register(WoundHealing)

