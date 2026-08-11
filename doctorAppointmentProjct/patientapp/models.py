import json
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from asgiref.sync import async_to_sync

from channels.layers import  get_channel_layer
import json




class homepageBanner(models.Model):
    mainHeading = models.CharField(max_length=100)
    subHeading = models.CharField(max_length=200)
    context = models.TextField()
    bannerImage = models.ImageField(upload_to="bannerImage")
    




class patientProfile(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    fullName = models.CharField(max_length=100,blank=True,null=True)
    mobile = models.IntegerField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    pinCode = models.CharField(max_length=15,blank=True,null=True)
    aboutPatient = models.TextField(blank=True,null=True)
    photoPatient = models.ImageField(upload_to="patientPhoto",blank=True,null=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True,null=True)




class doctorServices(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="servicePhoto")
    created_date = models.DateTimeField(auto_now_add=True)




class doctorProfile(models.Model):
    user = models.OneToOneField(to=User,on_delete=models.CASCADE)
    fullName = models.CharField(max_length=100,blank=True,null=True)
    mobile = models.IntegerField(blank=True,null=True)
    education = models.CharField(max_length=100,blank=True,null=True)
    speciality = models.CharField(max_length=100,blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    city = models.CharField(max_length=50,blank=True,null=True)
    state = models.CharField(max_length=50,blank=True,null=True)
    country = models.CharField(max_length=50,blank=True,null=True)
    pinCode = models.CharField(max_length=15,blank=True,null=True)
    aboutDoctor = models.TextField(blank=True,null=True)
    photoDoctor = models.ImageField(upload_to="photoDoctor",blank=True,null=True)
    createdDate = models.DateTimeField(auto_now_add=True, blank=True,null=True)




class ourTeam(models.Model):
    name = models.CharField(max_length=100)
    about = models.TextField()
    teamMemberPhoto = models.ImageField(upload_to = "t4eamMemberPhoto",blank=True,null=True)





class patientReviews(models.Model):
    patient = models.ForeignKey(to=patientProfile,on_delete=models.CASCADE)
    text = models.TextField()
    createdDate = models.DateTimeField(auto_now_add=True)





class patientAppointment(models.Model):
    patient = models.ForeignKey(to=patientProfile,on_delete=models.CASCADE)
    doctor = models.ForeignKey(to=doctorProfile,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.IntegerField()
    date = models.DateField()
    time = models.TimeField(blank=True,null=True)
    doctorAccept = models.BooleanField(default=False)
    doctorCompleted  = models.BooleanField(default=False)
    patientFeedback = models.TextField(blank=True,null=True)
    doctorReject = models.BooleanField(default=False)



class patientFeedback(models.Model):
    appointment = models.ForeignKey(to=patientAppointment,on_delete=models.CASCADE)
    feedbackText = models.TextField()


class Disease_predicted_data(models.Model):
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)
    reult_predicted = models.CharField(max_length=100)
    is_seen = models.BooleanField(default=False,null=True,blank=True)

    # def save(self,*args,**kwargs):
    #     print("save override")

    #     channel_layer = get_channel_layer()
    #     notification_objs = Disease_predicted_data.objects.filter(is_seen=False).count()

    #     data = {
    #         'count': notification_objs,
    #         'current_notification': self.Disease_predicted_data
    #     }

    #     async_to_sync(channel_layer.group_send)(
    #         'test_consumer_group', {
    #             'type' : 'send_notification',
    #             'value' : json.json.dumps(data)
    #         }
    #     )

        # super(Disease_predicted_data,self).save(*args,**kwargs)



