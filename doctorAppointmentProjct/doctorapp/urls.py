from django.urls import path
from .views import *
urlpatterns = [
    
    path('doctor-dashboard',doctor_dashboard,name="doctor-dashboard"),
    path('doctor-login',doctor_login,name="doctor-login"),
    path('doctor-logout',doctor_logout,name="doctor-logout"),
    path('doctor-profile',doctor_profile,name="doctor-profile"),
    path('doctor-appointments',doctor_appointments,name="doctor-appointments"),
    path('doctor-feedbacks',doctor_feedbacks,name="doctor-feedbacks"),
    path('doctor-patients-list',doctor_patient_list,name="doctor-patients-list"),
    path('doctor-patient-detail',doctor_patient_detail,name="doctor-patient-detail"),
    path('doctor-add-prescription',doctor_add_prescription,name="doctor-add-prescription"),
    path('doctor-add-notification',doctor_add_notification,name="doctor-add-notification"),
    path('doctor-messages',doctor_messages,name="doctor-messages"),
    path('reject_appointment/<int:myid>/',reject_appointment,name="reject_appointment"),
    path('accept_appointment/<int:myid>/',accept_appointment,name="accept_appointment"),
    path('complete_appointment/<int:myid>/',complete_appointment,name="complete_appointment"),

    path('doctor_profile',doctor_profile,name="doctor_profile"),
    path('update_doctor_photo',update_doctor_photo,name="update_doctor_photo"),
    path('save_doctor_profile',save_doctor_profile,name="save_doctor_profile"),


    # path('',,name=""),
   


]
