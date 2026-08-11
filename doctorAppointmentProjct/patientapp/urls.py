from django.urls import path
from .views import *

urlpatterns = [

    path('base',base,name="base"),
    path('',index,name="index"),
    path('services',services,name="services"),
    path('services_detail/<int:myid>/',services_detail,name="services_detail"),
    path('doctors',doctors,name="doctors"),
    path('about',about,name="about"),
    path('contact-us',contact_us,name="contact-us"),
    path('register',register,name="register"),
    path('login',login,name="login"),
    path('logout',logout,name="logout"),
    path('my-profile',my_profile,name="my-profile"),
    path('make-appointment/<int:doctor_id>/',make_appointment,name="make-appointment"),
    path('appointment_sent/<int:doctor_id>/',appointment_sent,name="appointment_sent"),
    path('patient-dashboard',patient_dashboard,name="patient-dashboard"),
    path('save_profile',save_profile,name="save_profile"),
    path('update_photo',update_photo,name="update_photo"),

    path('appointments',appointments,name="appointments"),
    path('update-profile',update_profile,name="update-profile"),
    path('update-profile-photo',update_profile_photo,name="update-profile-photo"),
    path('filter-doctor',filter_doctor,name="filter-doctor"),
    path('doctor-detail/<int:myid>/',doctor_detail,name="doctor-detail"),
    path('feedback',feedback,name="feedback"),
    path('send_feedback/<int:myid>/',send_feedback,name="send_feedback"),
    path('change-password',change_password,name="change-password"),
    path('change-password-done',change_password_done,name="change-password-done"),
    path('disease-prediction',disease_prediction,name="disease-prediction"),
    path('success-predict-disease',success_predict_disease,name="success-predict-disease"),

    path('check_disease',check_disease,name="check_disease"),
    path('predict_disease',predict_disease,name="predict_disease"),
    path('generate-pdf-report/', generate_pdf_report, name='generate_pdf_report'),
]
