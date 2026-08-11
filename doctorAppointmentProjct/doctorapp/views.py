from django.shortcuts import render, redirect,HttpResponse

from django.http import request
from django.http.response import JsonResponse
from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import os

from patientapp.views import appointments
from .models import *
from patientapp .models import *
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
# Create your views here.


@login_required(login_url='doctor-login')
def doctor_dashboard(request):
    user = request.user
    doctorObj= doctorProfile.objects.get(user = user)

    pat_id = []
    all_app = patientAppointment.objects.filter(doctor = doctorObj)
    for i in all_app:
        pat_id.append(i.patient.id)
    pat_l = set(pat_id)
    patient_ids = list(pat_l)
    patientProfileObj = patientProfile.objects.filter(id__in = patient_ids)
    print(patientProfileObj)


    appointmentObj = patientAppointment.objects.filter(doctor = doctorObj)
    context = {
        'appointments': appointmentObj,
        'patient':patientProfileObj,

    }
    return render(request,'doctorapp/doctor-dashboard.html',context)




def doctor_profile(request):
    user = request.user
    doctorProfileObj= doctorProfile.objects.get(user = user)
    context = {
        'doctor':doctorProfileObj
    }
    return render(request,'doctorapp/doctor-profile.html',context)




def save_doctor_profile(request):
    if request.method == "POST":
        user = request.user
        doctorProfileObj = doctorProfile.objects.get(user = user)

        doctorProfileObj.fullName = request.POST['fullName']
        doctorProfileObj.mobile = request.POST['mobile']
        doctorProfileObj.education = request.POST['education']
        doctorProfileObj.speciality = request.POST['speciality']
        doctorProfileObj.address = request.POST['address']
        doctorProfileObj.city = request.POST['city']
        doctorProfileObj.state = request.POST['state']
        doctorProfileObj.country = request.POST['country']
        doctorProfileObj.pinCode = request.POST['pinCode']
        doctorProfileObj.aboutDoctor = request.POST['aboutDoctor']
        
        doctorProfileObj.save()
        messages.info(request,"Profile updated successfully..")
    else:
        messages.info(request,"something wrong")
    return redirect('doctor_profile')



def update_doctor_photo(request):
    if request.method == "POST":
        user = request.user
        doc = doctorProfile.objects.get(user = user)

        photo = request.FILES['photoDoctor']
        doc.photoDoctor = photo
        doc.save()
        messages.info(request,"Photo updated successfully..")

    else:
        pass
    return redirect('doctor-profile')





def reject_appointment(request,myid):
    appointmentObj = patientAppointment.objects.get(id = myid)
    appointmentObj.doctorReject = True
    appointmentObj.save()
    messages.info(request,"Appointment Rejected successfully")
    return redirect('doctor-dashboard')





def accept_appointment(request,myid):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    appointmentObj = patientAppointment.objects.get(id = myid)
    appointmentObj.doctorAccept = True
    appointmentObj.time = current_time
    appointmentObj.save()

    messages.info(request,"Appointment Accepted successfully")
    return redirect('doctor-dashboard')




def complete_appointment(request,myid):
    appointmentObj = patientAppointment.objects.get(id = myid)
    appointmentObj.doctorCompleted = True
    appointmentObj.save()
    messages.info(request,"Appointment Completeed  successfully")

    return redirect('doctor-dashboard')




def doctor_login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                if doctorProfile.objects.get(user = user):
                    print("User is Doctor")
                    auth.login(request,user)
                    return redirect("doctor-dashboard")
                else:
                    print("User is not doctor")
                    messages.info(request,'You are not Doctor account')
                    return render(request,'doctorapp/doctor-login.html')
            except:
                messages.info(request,'You are not Doctor account')
                return render(request,'doctorapp/doctor-login.html')
        else:
            messages.info(request,'invalid credentials')
            return render(request,'doctorapp/doctor-login.html')
    else:    
        return render(request,'doctorapp/doctor-login.html')



    # return render(request,'doctorapp/doctor-login.html')








def doctor_appointments(request):
    return render(request,'doctorapp/')






def doctor_feedbacks(request):
    return render(request,'doctorapp/')






def doctor_patient_list(request):
    return render(request,'doctorapp/')






def doctor_patient_detail(request):
    return render(request,'doctorapp/')






def doctor_add_prescription(request):
    return render(request,'doctorapp/')





def doctor_logout(request):
    user = request.user
    auth.logout(request)
    return redirect('doctor-login')






def doctor_add_notification(request):
    return render(request,'doctorapp/')






def doctor_messages(request):
    return render(request,'doctorapp/')





# def (request):
#     return render(request,'doctorapp/')





