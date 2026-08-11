from django.contrib import admin

from patientapp.models import Disease_predicted_data, doctorProfile, doctorServices, homepageBanner, ourTeam, patientAppointment, patientFeedback, patientProfile, patientReviews

# Register your models here.
admin.site.register(patientProfile)
admin.site.register(doctorServices)
admin.site.register(doctorProfile)
admin.site.register(ourTeam)
admin.site.register(patientReviews)
admin.site.register(homepageBanner)
admin.site.register(patientAppointment)
admin.site.register(patientFeedback)

admin.site.register(Disease_predicted_data)