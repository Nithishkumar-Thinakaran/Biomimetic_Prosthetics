from django.contrib import messages
from django.shortcuts import render,redirect
from client.models import requirement, registration

def IH_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        if email=="emp1@gmail.com" and password=="emp1":
            messages.info(request,"Integrate Hub Login Successful")
            return redirect("/IH_home/")
        elif email !="emp1@gmail.com" and password=="emp1":
            messages.error(request, "Incorrect Username!")
            return render(request, "integratehub/integrate_hub_signup_login.html")
        elif email =="emp1@gmail.com" and password!="emp1":
            messages.error(request, "Incorrect Password!")
            return render(request, "integratehub/integrate_hub_signup_login.html")
        elif email !="emp1@gmail.com" and password!="emp1":
            messages.error(request, "Incorrect Username and Password!")
            return render(request,"integratehub/integrate_hub_signup_login.html")
        else:
            return render(request, "integratehub/integrate_hub_signup_login.html")
    return render(request, "integratehub/integrate_hub_signup_login.html")
def IH_home(request):
    return render(request,"integratehub/IH_home.html")

def IH_logout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        messages.success(request, 'Integrate Hub Logout successful')
        return redirect('/')
    else:
        messages.success(request, 'Integrate Hub Logout successful')
        return redirect('/')

def client_record(request):
    data=requirement.objects.all()
    return render(request,"integratehub/client_record.html",{'data':data})

def integration(request):
    data=requirement.objects.all()
    return render(request,"integratehub/integration.html",{'data':data})

import pandas as pd
# def integration_process(request, c_id):
#     data = requirement.objects.filter(c_id=c_id)
#     csv_path = r'D:\Projects\Biomimetic_Prosthetics\Material Dataset.csv'
#     df = pd.read_csv(csv_path)
#     for _, row in df.iterrows():
#         for i in data:
#             if (i.prosthetics_type) == (row['Application']):
#                 i.Biomimetic_Hydrogel = row['Biomimetic_Hydrogel']
#                 i.Key_Material = row['Key_Material']
#                 i.Application_Description = row['Application_Description']
#                 i.Key_Properties = row['Key_Properties']
#                 i.Manufacturing_Process = row['Manufacturing_Process']
#                 i.Clinical_Status = row['Clinical_Status']
#                 i.save()
#     d=registration.objects.get(c_id=c_id)
#     d.ihdone=True
#     d.save()
#     data1 = requirement.objects.get(c_id=c_id)
#     data1.ihdone1=True
#     data1.save()
#     messages.info(request, f"Integration Processing Progressed Successfully for {c_id}")
#     return render(request,"integratehub/integration.html",{'data':data})


import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.mail import EmailMessage

def integration_process(request, c_id):
    # Retrieve data from requirement model
    data = requirement.objects.filter(c_id=c_id)

    # Path to the CSV file containing material dataset
    csv_path = r'D:\Project_PG\Biomimetic_Prosthetics\Material Dataset.csv'

    # Read the material dataset CSV into a pandas DataFrame
    df_material = pd.read_csv(csv_path)

    # Iterate over rows in the material dataset
    for _, row_material in df_material.iterrows():
        for item in data:
            if item.prosthetics_type == row_material['Application']:
                # Fetch the requirement object again
                data_obj = requirement.objects.get(c_id=c_id)

                # Define the content to be written in the integration report
                title = "INTEGRATION PROCESSING"
                list_data = [
                    f"---------------------------------------------------------------------------------------------",
                    f"S.ID: {data_obj.c_id}",
                    f"prosthetics_type: {data_obj.prosthetics_type}",
                    f"---------------------------------------------------------------------------------------------",
                    f"Biomimetic Hydrogel: {row_material['Biomimetic_Hydrogel']}\n",
                    f"Key Material: {row_material['Key_Material']}\n",
                    f"Application Description Section Depth: {row_material['Application_Description']}\n",
                    f"Key Properties: {row_material['Key_Properties']}\n",
                    f"Manufacturing Process: {row_material['Manufacturing_Process']}\n",
                    f"Clinical Status: {row_material['Clinical_Status']} \n"
                ]

                csv_path1 = r'D:\Project_PG\Biomimetic_Prosthetics\Quantity Dataset.csv'
                df_quantity = pd.read_csv(csv_path1)
                for _, row_quantity in df_quantity.iterrows():
                    if item.prosthetics_type == row_quantity['Application']:
                        list_data.append(f"Biomimetic_Material: {row_quantity['Biomimetic_Material']}")
                        list_data.append(f"Quantity: {row_quantity['Quantity']} kg")

                content = f"{title}\n\n" + '\n'.join(list_data)
                file_content = ContentFile(content.encode('utf-8'))
                data_obj.Integrate_Hub_Report.save(f"{title}_{data_obj.c_id}.txt", file_content)
                data_obj.fview = True
                data_obj.save()
    registration_obj = registration.objects.get(c_id=c_id)
    registration_obj.ihdone = True
    registration_obj.status = "Integration Hub Done"
    registration_obj.save()
    data_obj = requirement.objects.get(c_id=c_id)
    data_obj.ihdone1 = True
    data_obj.save()

    subject = 'Confirmation of Successful Integration Hub Process Completion'
    message = f'Hi {registration_obj.name},\nWe are pleased to inform you that the Integration Hub Process has been successfully completed. Your requirements will be satisfied shortly, and we appreciate your patience.\n\nThank you for choosing our services.'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [registration_obj.email]

    email = EmailMessage(
        subject,
        message,
        email_from,
        recipient_list,
    )
    email.send()

    messages.info(request, f"Integration Processing Progressed Successfully for {c_id}")
    return redirect("/integration/", {'data': data})


def IH_Report(request):
    data=requirement.objects.filter(ihdone1=True)
    return render(request,"integratehub/IH_Report.html",{'data':data})