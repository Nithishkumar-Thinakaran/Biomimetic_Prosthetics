from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from client.models import registration, requirement


def index(request):
    return render(request,'index/index.html')

def client_signup_login(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        password=request.POST['password']
        registration(name=name, email=email,phone=phone, password=password).save()
        messages.info(request,f"{name} Registration Successful")
        return render(request,'client/client_signup_login.html')
    return render(request,'client/client_signup_login.html')

def client_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            s = registration.objects.get(email=email, password=password)
            if s.approve:
                messages.info(request, f"{s.name} Login Successful")
                request.session['user_id'] = s.c_id
                print( request.session['user_id'])
                s.login = True
                s.logout = False
                s.save()
                return redirect("/client_home/")
            else:
                messages.info(request, "You need Management Approval to Access the Client Portal")
                return render(request,'client/client_signup_login.html')

        except registration.DoesNotExist:
            messages.info(request, "Invalid Email or Password")

    return render(request,'client/client_signup_login.html')

def client_home(request):
    return render(request,"client/client_home.html")

def client_logout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        try:
            s = registration.objects.get(c_id=user_id)
            s.logout = True
            s.login = False
            s.save()
            del request.session['user_id']
            messages.success(request, 'Client Logout successful')
            return redirect('/')
        except registration.DoesNotExist:
            messages.error(request, 'User not found')

        request.session.pop('user_id', None)
    else:
        messages.info(request, 'Patient Logout successful')
    return redirect('/')



def client_req(request):
    try:
        data=registration.objects.get(login=True)
        d = data.c_id
        e= data.name
        c_data = requirement.objects.get(c_id=d)
        messages.info(request, "Record Already Uploaded!")
        return redirect("/client_home/")
    except:
        data = registration.objects.get(login=True)
        d = data.c_id
        e = data.name
        if request.method=="POST":
            c_id=d
            name=e
            gender=request.POST['gender']
            age=request.POST['age']
            height=request.POST['height']
            width=request.POST['width']
            medical_condition=request.POST['medical_condition']
            prosthetics_type=request.POST['prosthetics_type']

            requirement(c_id=c_id, name=name,gender=gender,age=age,height=height,width=width,
                           medical_condition=medical_condition,prosthetics_type=prosthetics_type).save()
            data.upload = True
            data.status="Record Uploaded...Process Pending"
            data.save()
            messages.info(request,f"{c_id} Requirement Upload Successful")
            return redirect("/client_home/")
        return render(request,"client/client_req.html",{'d':d,'e':e})

def checkpoints(request):
    try:
        data=registration.objects.get(login=True)
        c_id=data.c_id
        data1 = requirement.objects.get(c_id=c_id)
        return render(request,"client/checkpoints.html",{'data':data,'data1':data1})
    except:
        messages.info(request,f"{c_id} Record Not Yet Uploaded")
        return redirect('/client_home/')