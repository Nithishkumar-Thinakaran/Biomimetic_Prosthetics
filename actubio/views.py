from django.contrib import messages
from django.shortcuts import render,redirect

from client.models import requirement, registration


def AB_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if email=="emp3@gmail.com" and password=="emp3":
            messages.info(request,"ActuBio Login Successful")
            return redirect("/AB_home/")
        elif email !="emp3@gmail.com" and password=="emp3":
            messages.error(request, "Incorrect Username!")
            return render(request, "actubio/actubio_signup_login.html")
        elif email =="emp3@gmail.com" and password!="emp3":
            messages.error(request, "Incorrect Password!")
            return render(request, "actubio/actubio_signup_login.html")
        elif email !="emp3@gmail.com" and password!="emp3":
            messages.error(request, "Incorrect Username and Password!")
            return render(request,"actubio/actubio_signup_login.html")
        else:
            return render(request, "actubio/actubio_signup_login.html")
    return render(request, "actubio/actubio_signup_login.html")


def AB_logout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        messages.success(request, 'ActuBio Logout successful')
        return redirect('/')
    else:
        messages.success(request, 'ActuBio Logout successful')
        return redirect('/')


def AB_home(request):
    return render(request,"actubio/AB_home.html")

def BA_Record(request):
    data=requirement.objects.filter(badone2=True)
    return render(request,'actubio/BA_Record.html',{'data':data})



def AB_Process(request):
    data=requirement.objects.filter(badone2=True)
    return render(request,'actubio/AB_Process.html',{'data':data})




from django.shortcuts import render
from django.contrib import messages
import pandas as pd
from django.conf import settings
from django.core.mail import EmailMessage

#Specific_Surface_Area (m²/g)
# Control_Response Time (ms)
# Energy Density (kJ/kg)
# Weight (kg/m³)
def actubio_process(request, c_id):
    data = requirement.objects.filter(c_id=c_id)
    csv_path = r'D:\Project_PG\Biomimetic_Prosthetics\ActuBio Dataset.csv'
    df = pd.read_csv(csv_path)
    for _, row in df.iterrows():
        try:
            req = data.get(prosthetics_type=row['Application'])
            req.Actuation_Mechanism = row['Actuation_Mechanism']
            req.Biocompatibility_Factors = row['Biocompatibility_Factors']
            req.Typical_Force_Output_N = row['Typical_Force_Output_N']
            req.Specific_Surface_Area = row['Specific_Surface_Area']
            req.Control_Response_Time = row['Control_Response_Time']
            req.Energy_Density = row['Energy_Density']
            req.Weight_Actubio = row['Weight']
            req.save()
        except requirement.DoesNotExist:
            pass


    d = registration.objects.get(c_id=c_id)
    d.abdone = True
    d.status = "Actu-Bio Done"
    d.save()
    data1 = requirement.objects.get(c_id=c_id)
    data1.abdone3 = True
    data1.save()

    subject = 'Confirmation of Successful Actu-Bio Process Completion'
    message = f'Hi {d.name},\nWe are pleased to inform you that the Actu-Bio Process has been successfully completed. Your requirements will be satisfied shortly, and we appreciate your patience.\n\nThank you for choosing our services.'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [d.email]

    email = EmailMessage(
        subject,
        message,
        email_from,
        recipient_list,
    )
    email.send()

    messages.info(request, f"Actu-Bio Progressed Successfully for {c_id}")
    return redirect("/AB_Process/", {'data': data})


#Actu-Bio Report
def actu_bio_report(request):
    data=requirement.objects.filter(abdone3=True)
    return render(request,"actubio/AB_Report.html",{'data':data})