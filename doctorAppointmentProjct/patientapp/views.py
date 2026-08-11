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
from .models import *
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

########### ML REQUIRED
# Importing libraries
from sklearn.svm import SVC
import numpy as np
import pandas as pd
from scipy.stats import mode
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import joblib


#############

# Create your views here.



def isPatient(request):
    try:
        user = request.user
        print(user)
        if user.patientprofile:
            print("user found")
            return True
        else:
            print("not found")
            return False
    except:
        print("except")
        return False

def base(request):
    try:
        user = request.user
        print(user.patientProfile)
    except:
        pass
    return render(request,'patientapp/base.html')





def index(request):
    bannerObj = homepageBanner.objects.last()
    services = doctorServices.objects.all()[:3]
    reviewsObj = patientReviews.objects.all()[:3:-1]
    context = {
        'services' : services,
        'reviews':reviewsObj,
        'banner': bannerObj
    }
    return render(request,'patientapp/index.html',context)








def services(request):
    service_obj = doctorServices.objects.all()
    context = {
        'services':service_obj
    }

    return render(request,'patientapp/services.html',context)




def services_detail(request,myid):
    docServiceObj = doctorServices.objects.get(id = myid)
    context = {
        'service' : docServiceObj
    }
    return render(request,'patientapp/services_detail.html',context)



def doctors(request):
    doctor_obj = doctorProfile.objects.all()
    context = {
        'doctors' : doctor_obj
    }
    return render(request,'patientapp/doctors.html',context)






def about(request):
    ourTeamObj = ourTeam.objects.all()
    context = {
        'team_members' : ourTeamObj
    }
    return render(request,'patientapp/about.html',context)




def contact_us(request):
    return render(request,'patientapp/contact-us.html')




def register(request):

    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['pass']
        password2 = request.POST['cpass']


        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username already taken")
                return redirect('register')

            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email-id already taken")
                return redirect('register')
            else:
                
                user = User.objects.create_user(username=username,email=email,password = password1,first_name = fname,last_name=lname)
                user.save()
                auth.login(request,user)
                pat_pro = patientProfile.objects.create(user = user)
                pat_pro.save()
                return redirect('/')
                   
        else:
            messages.info(request," Bboth Password are not match")
            return redirect('register')
    else:
        return render(request, 'patientapp/register.html')




    # return render(request,'patientapp/register.html')




def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']

        user=auth.authenticate(username=username, password=password)
        if user is not None:
            try:
                if patientProfile.objects.get(user = user):
                    print("User is patient")
                    auth.login(request,user)
                    return redirect("/")
                else:
                    print("User is not patient")
                    messages.info(request,'You are not patient account')
                    return render(request,'patientapp/login.html')
            except:
                messages.info(request,'You are not patient account')
                return render(request,'patientapp/login.html')
        else:
            messages.info(request,'invalid credentials')
            return redirect("login")
    else:    
        return render(request,'patientapp/login.html')



    # return render(request,'patientapp/login.html')





def logout(request):
    user = request.user
    auth.logout(request)
    return redirect('login')








@login_required(login_url="login")
def my_profile(request):
    if isPatient(request):
        user = request.user
        patientProfileObj = patientProfile.objects.get(user = user)
        context = {
            'patient':patientProfileObj
        }
        return render(request,'patientapp/my-profile.html',context)
    else:
        return redirect('login')





@login_required(login_url="login")
def make_appointment(request,doctor_id):
    if isPatient(request):
        user = request.user
        doctorObj = doctorProfile.objects.get(id = doctor_id)
        context = {
            'doctor': doctorObj
        }
        return render(request,'patientapp/make-appointment.html',context)
    else:
        return redirect('login')



@login_required(login_url="login")
def appointment_sent(request,doctor_id):
    try:
        if isPatient(request):
            if request.method == "POST":
                user = request.user
                print(request.META.get('HTTP_REFERER'))
                patientObj = patientProfile.objects.get(user = user)
                doctorObj = doctorProfile.objects.get(id = doctor_id)

                full_name = request.POST['full_name']
                email = request.POST['email']
                mobile = request.POST['mobile']
                date = request.POST['date']

                appointmentObj = patientAppointment(patient =patientObj,doctor = doctorObj,name = full_name,email=email,mobile=mobile,date = date)
                appointmentObj.save()
                messages.info(request,"Your appointment Booked successfully")
                return redirect(request.META.get('HTTP_REFERER'))
            else:
                messages.info(request,"Something webt wrong")
                return redirect(request.META.get('HTTP_REFERER'))
        else:
            return redirect('login')
    except:
        messages.info(request,"Login First then book appointment")
        return redirect(request.META.get('HTTP_REFERER'))



@login_required(login_url="login")
def patient_dashboard(request):
    if isPatient(request):
        user = request.user
        if user.patientprofile.user:
            patientObj = patientProfile.objects.get(user = user)
            appointmentObj = patientAppointment.objects.filter(patient = patientObj)
            patientFeedbackObj = patientFeedback.objects.all()

            context = {
                'appointments': appointmentObj,
                'feedback': patientFeedbackObj
            }

            return render(request,'patientapp/patient-dashboard.html',context)
        else:
            return redirect('login')
    else:
        return redirect('login')





@login_required(login_url="login")
def appointments(request):
    return render(request,'patientapp/appointments.html')







@login_required(login_url="login")
def update_profile(request):
    return render(request,'patientapp/')





@login_required(login_url="login")
def update_profile_photo(request):
    return render(request,'patientapp/')






def filter_doctor(request):
    doctorProfileObj = doctorProfile.objects.filter(fullName__icontains = request.GET['doctor_name'])
    context = {
        'doctors' : doctorProfileObj
    }
    return render(request,'patientapp/doctors.html',context)






def doctor_detail(request,myid):
    doctorObj = doctorProfile.objects.get(id = myid)
    context = {
        'doctor':doctorObj
    }
    return render(request,'patientapp/doctor-detail.html',context)





def feedback(request):
    return render(request,'patientapp/')





@login_required(login_url="login")
def save_profile(request):
    if isPatient(request):
        if request.method == "POST":
            user = request.user
            patientProfileObj = patientProfile.objects.get(user = user)
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            patientProfileObj.fullName = request.POST["fname"] + " "+request.POST['lname']
            patientProfileObj.mobile = request.POST["mobile"]
            patientProfileObj.address =request.POST["address"]
            patientProfileObj.city = request.POST["city"]
            patientProfileObj.state = request.POST["state"]
            patientProfileObj.country = request.POST["country"]
            patientProfileObj.pinCode = request.POST["pinCode"]
            patientProfileObj.patientAbout = request.POST["patientAbout"]
            user.save()
            patientProfileObj.save()
            messages.info(request,"patient Profile Updated successfully")
            return redirect('my-profile')

        else:
            return redirect('my-profile')
    else:
        return redirect('login')



@login_required(login_url="login")
def update_photo(request):
    if isPatient(request):
        if request.method == "POST":
            user = request.user
            patientProfileObj = patientProfile.objects.get(user=user)

            photoPatient = request.FILES['photoPatient']
            patientProfileObj.photoPatient = photoPatient
            patientProfileObj.save()
            messages.info(request,"Profile photo Updated")

        else:
            pass
        return redirect('my-profile')
    else:
        return redirect('login')


@login_required(login_url="login")
def send_feedback(request,myid):
    if isPatient(request):
        if request.method == "POST":
            print(myid)
            print(request.POST["feedback_text"])
            appointmentObj = patientAppointment.objects.get(id = myid)
            # patientFeedbackObj = patientFeedback(appointment = appointmentObj,feedbackText = request.POST['feedback_text'])
            # patientFeedbackObj.save()
            appointmentObj.patientFeedback = request.POST['feedback_text']
            appointmentObj.save()
            print('submited')
            messages.info(request,'your feedback submitted successfully')
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect('login')





@login_required(login_url="login")
def change_password(request):
    return render(request,'patientapp/change-password.html')





@login_required(login_url="login")
def change_password_done(request):
    try:
        user = request.user
        if request.method == "POST":
            old_password = request.POST['old_pass']
            new_password = request.POST['new_pass']
            confirm_new_password = request.POST['confirm_new_pass']
            if user.check_password(old_password):
                if new_password == confirm_new_password:
                    user.set_password(new_password)
                    user.save()
                    if user is not None:
                        auth.login(request,user)
                    messages.success(request,"Password Changes Successfully ! ")
                else:
                    messages.info(request,"Password not matching ! ")
            else:
                messages.error(request,"Old Password is not correctt ! ")
        else:
            pass
        return redirect('change-password')
    except:
        return HttpResponse("Something wrong")








def disease_prediction(request):
    return render(request,'patientapp/')





def success_predict_disease(request):
    return render(request,'patientapp/')





@login_required(login_url="login")
def check_disease(request):
    return render(request,'patientapp/check_disease.html')



@login_required(login_url="login")
def predict_disease(request):
    if request.method == "POST":
        # Load from file
        user = request.user
        joblib_model = joblib.load("final_disease_predict_model.pkl")
        prediction = joblib_model .predict([[
            request.POST['itching'],
            request.POST['skin_rash'],
            request.POST['nodal_skin_eruptions'],
            request.POST['continuous_sneezing'],
            request.POST['shivering'],
            request.POST['shivering'],
            request.POST['joint_pain'],
            request.POST['stomach_pain'],
            request.POST['acidity'],
            request.POST['ulcers_on_tongue'],
            request.POST['muscle_wasting'],
            request.POST['vomiting'],
            request.POST['burning_micturition'],
            request.POST['spotting_urination'],
            request.POST['fatigue'],
            request.POST['weight_gain'],
            request.POST['anxiety'],
            request.POST['cold_hands_and_feets'],
            request.POST['mood_swings'],
            request.POST['weight_loss'],
        ]])
        print(prediction)
        result = ""
        if prediction == 1:
            result = "Paroymsal  Positional Vertigo"
        elif prediction == 2:
            result = "AIDS"
        elif prediction == 3:
            result = "Acne"
        elif prediction == 4:
            result = "Alcoholic hepatitis"
        elif prediction == 5:
            result = "Allergy"
        elif prediction == 6:
            result = "Arthritis"
        elif prediction == 7:
            result = "Bronchial Asthma"
        elif prediction == 8:
            result = "Cervical spondylosis"
        elif prediction == 9:
            result = "Chicken pox"
        elif prediction == 10:
            result = "Chronic cholestasis"
        elif prediction == 11:
            result = "Common Cold"
        elif prediction == 12:
            result = "Dengue"
        elif prediction == 13:
            result = "Diabetes"
        elif prediction == 14:
            result = "Dimorphic hemmorhoids(piles)"
        elif prediction == 15:
            result = "Drug Reaction"
        elif prediction == 16:
            result = "Fungal infection"
        elif prediction == 17:
            result = "GERD"
        elif prediction == 18:
            result = "Gastroenteritis"
        elif prediction == 19:
            result = "Heart attack"
        elif prediction == 20:
            result = "Hepatitis C"
        elif prediction == 21:
            result = "Hepatitis D"
        elif prediction == 22:
            result = "Hepatitis E"
        elif prediction == 23:
            result = "Hypertension"
        elif prediction == 24:
            result = "Hyperthyroidism"
        elif prediction == 25:
            result = "Hypoglycemia"
        elif prediction == 26:
            result = "Hypothyroidism"
        elif prediction == 27:
            result = "Impetigo"
        elif prediction == 28:
            result = "Jaundice"
        elif prediction == 29:
            result = "Malaria"
        elif prediction == 30:
            result = "Migraine"
        elif prediction == 31:
            result = "Osteoarthristis"
        elif prediction == 32:
            result = "Paralysis (brain hemorrhage)"
        elif prediction == 33:
            result = "Peptic ulcer diseae"
        elif prediction == 34:
            result = "Pneumonia"
        elif prediction == 35:
            result = "Psoriasis"
        elif prediction == 36:
            result = "Tuberculosis"
        elif prediction == 37:
            result = "Typhoid"
        elif prediction == 38:
            result = "Urinary tract infection"
        elif prediction == 39:
            result = "Varicose veins"
        elif prediction == 40:
            result = "hepatitis A"
        else:
            result = "cant predict"
        print(result)
        Disease_predicted_data_obj = Disease_predicted_data(user = user,reult_predicted = result)
        print(Disease_predicted_data_obj)
        Disease_predicted_data_obj.save()
        messages.info(request,f"predicted disease is {result}")
        return redirect('check_disease')
        # return HttpResponse("Import success")


from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime
import io


# @login_required  # Comment this out temporarily if you're getting auth issues
def generate_pdf_report(request):
    """
    Generate PDF report for disease prediction results
    """
    try:
        # Create the HttpResponse object with PDF headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Sympwise_report.pdf"'

        # Create PDF document
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        story = []

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.darkblue
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            textColor=colors.darkgreen
        )

        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=12,
            spaceAfter=12
        )

        # Title
        story.append(Paragraph("SYMPWISE REPORT", title_style))
        story.append(Spacer(1, 20))

        # Report Date
        current_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        story.append(Paragraph(f"<b>Report Generated:</b> {current_date}", normal_style))
        story.append(Spacer(1, 20))

        # User Details Section
        story.append(Paragraph("PATIENT INFORMATION", heading_style))
        user_data = [
            ['Name:', getattr(request.user, 'get_full_name', lambda: 'N/A')() or request.user.username],
            ['Email:', request.user.email or 'N/A'],
            ['Username:', request.user.username],
            ['Date Joined:',
             request.user.date_joined.strftime("%B %d, %Y") if hasattr(request.user, 'date_joined') else 'N/A']
        ]

        user_table = Table(user_data, colWidths=[2 * inch, 4 * inch])
        user_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))

        story.append(user_table)
        story.append(Spacer(1, 20))

        # Prediction Results Section
        story.append(Paragraph("DISEASE PREDICTION RESULTS", heading_style))

        # Get the referer URL to check if coming from prediction page
        referer = request.META.get('HTTP_REFERER', '')

        # Try to get the prediction message from URL parameters or form data
        prediction_message = request.GET.get('prediction', 'No recent prediction available')

        # If no prediction in URL, show a generic message
        if prediction_message == 'No recent prediction available':
            prediction_message = "Please run a disease prediction first to generate a detailed report."

        story.append(Paragraph(f"<b>Predicted Condition:</b> {prediction_message}", normal_style))
        story.append(Spacer(1, 20))

        # Common Recommended Next Steps
        story.append(Paragraph("RECOMMENDED NEXT STEPS", heading_style))
        recommendations = [
            "1. Consult with a qualified healthcare professional for proper diagnosis",
            "2. Provide complete medical history to your doctor",
            "3. Follow prescribed medication and treatment plans",
            "4. Maintain a healthy lifestyle with proper diet and exercise",
            "5. Monitor symptoms and report any changes to your healthcare provider",
            "6. Schedule regular follow-up appointments as recommended"
        ]

        for recommendation in recommendations:
            story.append(Paragraph(recommendation, normal_style))

        story.append(Spacer(1, 30))

        # Disclaimer Section
        story.append(Paragraph("IMPORTANT DISCLAIMER", heading_style))
        disclaimer_text = """
        <b>MEDICAL DISCLAIMER:</b><br/><br/>
        This report is generated by an AI-based prediction system and is intended for informational purposes only. 
        The predictions and recommendations provided are not a substitute for professional medical advice, diagnosis, or treatment.<br/><br/>

        <b>Please note:</b><br/>
        • Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition<br/>
        • Never disregard professional medical advice or delay seeking it because of information provided in this report<br/>
        • This system has limitations and may not detect all conditions or provide accurate predictions in all cases<br/>
        • Emergency situations require immediate medical attention - contact emergency services if needed<br/><br/>

        <b>Data Privacy:</b> Your personal health information is confidential and protected. This report should be shared only with authorized healthcare professionals.<br/><br/>

        <i>SYMPWISE - Your Digital Health Companion</i>
        """

        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=6,
            textColor=colors.red
        )

        story.append(Paragraph(disclaimer_text, disclaimer_style))

        # Build PDF
        doc.build(story)

        # Get the PDF data
        pdf_data = buffer.getvalue()
        buffer.close()

        response.write(pdf_data)
        return response

    except Exception as e:
        # Handle any errors and return a proper response
        from django.shortcuts import redirect
        from django.contrib import messages
        messages.error(request, f"Error generating PDF: {str(e)}")
        return redirect('check_disease')  # Replace with your actual URL name