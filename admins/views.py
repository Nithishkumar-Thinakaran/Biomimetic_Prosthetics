from django.contrib import messages
from django.shortcuts import render,redirect
import random
from client.models import registration, requirement
# from integratehub.models import employee


def admins_login(request):
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        if username=="admin" and password=="admin":
            messages.info(request,"Admin Login Successful")
            return redirect("/admins_home/")
        elif username !="admin" and password=="admin":
            messages.error(request, "Incorrect Username!")
            return render(request, 'admins/admins_login.html')
        elif username =="admin" and password!="admin":
            messages.error(request, "Incorrect Password!")
            return render(request, 'admins/admins_login.html')
        elif username !="admin" and password!="admin":
            messages.error(request, "Incorrect Username and Password!")
            return render(request,'admins/admins_login.html')
        else:
            return render(request, 'admins/admin_login.html')
    return render(request, 'admins/admins_login.html')

def admins_logout(request):
    if 'user_id' in request.session:
        request.session.pop('user_id',None)
        messages.success(request,'Admin Logout successful')
        return redirect('/')
    else:
        messages.success(request, 'Admin Logout successful')
        return redirect('/')

def admins_home(req):
    return render(req,"admins/admins_home.html")

def client_reg(request):
    data=registration.objects.all()
    return render(request,"admins/client_reg.html",{'data':data})


def approve(request, id):
    datas =registration.objects.get(id=id)
    p = random.randint(10000, 50000)
    datas.c_id = f"CLI:{p}"
    print(p)
    datas.approve = True
    datas.reject = False
    datas.save()
    messages.info(request, f"Client [{datas.c_id}] Approval Successful")
    return redirect('/admins_home/')

def reject(request, id):
    datas =registration.objects.get(id=id)
    datas.reject = True
    datas.approve = False
    datas.save()
    messages.info(request, "Client Registration Rejected")
    return redirect('/admins_home/')


#Integrate Hub
def IH_Result(request):
    data=requirement.objects.filter(ihdone1=True)
    return render(request,'admins/IH_Result.html',{'data':data})

#Bio Analysis
def BA_Result(request):
    data=requirement.objects.filter(badone2=True)
    return render(request,'admins/BA_Result.html',{'data':data})


#Actu-Bio Report
def AB_Result(request):
    data=requirement.objects.filter(abdone3=True)
    return render(request,"admins/AB_Result.html",{'data':data})
def authorize_report(request):
    data=requirement.objects.filter(abdone3=True)
    return render(request,"admins/authorize_report.html",{'data':data})



from reportlab.lib.colors import red, black
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.contrib import messages


def view_final_report(request, c_id):
    try:
        data = requirement.objects.get(c_id=c_id)
    except requirement.DoesNotExist:
        messages.error(request, f"Requirement with ID {c_id} does not exist.")
        return redirect('/authorize_report/')

    title = "BIOMIMETIC PROSTHETICS REPORT"
    list_data = [
        f"S.ID: {data.c_id}",
        "REQUIREMENTS",
        f"Name: {data.name}",
        f"Medical Condition: {data.medical_condition}",
        f"Prosthetics Type: {data.prosthetics_type}",

        "BIO-ANALYSIS",
        f"Material Composition: {data.Material_Composition}",
        f"Age of Application Years: {data.Age_of_Application_years}",
        f"Usage Frequency Times/Day: {data.Usage_Frequency_times_day}",
        f"Impact Resistance: {data.Impact_Resistance}",
        f"Wear Resistance: {data.Wear_Resistance}",
        f"Corrosion Resistance: {data.Corrosion_Resistance}",
        f"Temperature Resistance: {data.Temperature_Resistance}",
        f"Integrity: {data.Integrity}",
        f"Weight: {data.Weight}",
        f"Characteristics: {data.Characteristics}",
        f"Integrity Level (Prediction): {data.Integrity_Level_Pre}",

        "ACTUBIO",
        f"Actuation Mechanism: {data.Actuation_Mechanism}",
        f"Biocompatibility Factors: {data.Biocompatibility_Factors}",
        f"Typical Force Output N: {data.Typical_Force_Output_N}",
        f"Specific Surface Area: {data.Specific_Surface_Area}",
        f"Control Response Time: {data.Control_Response_Time}",
        f"Energy Density: {data.Energy_Density}",
        f"Weight Actubio: {data.Weight_Actubio}",
    ]

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 16)
    text_width = c.stringWidth(title)
    x_position = (c._pagesize[0] - text_width) / 2
    c.setFillColor(red)
    c.drawString(x_position, 800, title)

    c.setFont("Helvetica", 12)
    y_position = 780
    for line in list_data:
        if "S.ID: {data.c_id}" in line:
            c.setFillColor(black)
        else:
            c.setFillColor(black)
        if "REQUIREMENTS" in line or "BIO-ANALYSIS" in line or "ACTUBIO" in line:
            c.setFillColor(red)
        c.drawString(100, y_position, line)
        y_position -= 25


    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title}_{data.c_id}.pdf"'
    response.write(pdf_data)

    data.bp_final_report.save(f"{title}_{data.c_id}.pdf", ContentFile(pdf_data))
    data.finalreportview = True
    data.save()

    try:
        data1 = registration.objects.get(c_id=c_id)
        data1.status = "Final Report Generated"
        data1.save()
    except registration.DoesNotExist:
        messages.error(request, f"Registration with ID {c_id} does not exist.")

    messages.info(request, f"{data.c_id} Report Generated Successfully")
    return redirect('/authorize_report/')


def finalreportapprove(request, c_id):
    datas = requirement.objects.get(c_id=c_id)
    data = registration.objects.get(c_id=c_id)
    data.final = True
    data.status="Deployment Successful..!"
    datas.finalreportapprove = True
    datas.finalreportreject = False
    data.save()
    datas.save()

    subject = 'Biomimetic Prosthetics Report'
    message = f'Hi {data.name},\nYour Biomimetic Prosthetics Report has been Successfully Generated. We hope this report helps you gain valuable insights. \nThank you for choosing our Web Application.'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.email]

    email = EmailMessage(
        subject,
        message,
        email_from,
        recipient_list,
    )

    pdf_data = datas.bp_final_report.read()
    txt_data=datas.Integrate_Hub_Report.read()
    email.attach(f"{datas.c_id}.pdf", pdf_data, 'application/pdf')
    email.attach(f"{datas.c_id}.txt", txt_data, 'application/txt')
    email.send()

    messages.info(request, f"{datas.c_id} Biomimetic Prosthetics Report Approved and Sent Successful")
    return redirect('/authorize_report/')

from django.conf import settings
from django.core.mail import EmailMessage

def finalreportreject(request, c_id):
    datas = requirement.objects.get(c_id=c_id)
    datas.finalreportapprove = False
    datas.finalreportreject = False

    datas.ihdone1=False
    datas.badone2=False
    datas.abdone3=False
    datas.finalreportview=False
    datas.save()

    data = registration.objects.get(c_id=c_id)
    data.final = False
    data.status="Process Pending"
    data.ihdone=False
    data.badone=False
    data.abdone=False
    data.save()


    subject = 'Important: Admin Decision on Biomimetic Prosthetics Process'
    message = f'Hi {data.name},\nWe regret to inform you that your Biomimetic Prosthetics Process has been rejected by the Administrative Team. Due to unforeseen circumstances, we kindly request your patience and understanding.\nRest assured, we are diligently working to process your requirement and will provide an update shortly.\n\nThank you for choosing our Web Application.'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data.email]

    email = EmailMessage(
        subject,
        message,
        email_from,
        recipient_list,
    )

    email.send()

    messages.info(request, f"{datas.c_id} Biomimetic Prosthetics Report Rejected and Mail Sent to Client.")
    return redirect('/authorize_report/')
