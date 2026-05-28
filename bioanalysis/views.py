from django.shortcuts import render,redirect
from client.models import requirement, registration

def BA_home(request):
    return render(request,"bioanalysis/BA_home.html")

def BA_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        if email=="emp2@gmail.com" and password=="emp2":
            messages.info(request,"Bio Analysis Login Successful")
            return redirect("/BA_home/")
        elif email !="emp2@gmail.com" and password=="emp2":
            messages.error(request, "Incorrect Username!")
            return render(request, "bioanalysis/bioanalysis_signup_login.html")
        elif email =="emp2@gmail.com" and password!="emp2":
            messages.error(request, "Incorrect Password!")
            return render(request, "bioanalysis/bioanalysis_signup_login.html")
        elif email !="emp2@gmail.com" and password!="emp2":
            messages.error(request, "Incorrect Username and Password!")
            return render(request,"bioanalysis/bioanalysis_signup_login.html")
        else:
            return render(request, "bioanalysis/bioanalysis_signup_login.html")
    return render(request, "bioanalysis/bioanalysis_signup_login.html")


def BA_logout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        messages.success(request, 'Bio Analysis Logout successful')
        return redirect('/')
    else:
        messages.success(request, 'Bio Analysis Logout successful')
        return redirect('/')


#Integrate Hub
def IntegrateHub_Report(request):
    data=requirement.objects.filter(ihdone1=True)
    return render(request,'bioanalysis/IntegrateHub_Report.html',{'data':data})

#Bioanalysis
def bioanalysis(request):
    data=requirement.objects.filter(ihdone1=True)
    return render(request,'bioanalysis/bioanalysis.html',{'data':data})

#
# from django.shortcuts import render
# from django.contrib import messages
# import pandas as pd
# from sklearn.linear_model import LinearRegression
# from sklearn.preprocessing import StandardScaler
# from sklearn.pipeline import make_pipeline
# from sklearn.random_projection import GaussianRandomProjection
# from sklearn.model_selection import train_test_split
# from django.conf import settings
# from django.core.mail import EmailMessage
# def bioanalysis_process(request, c_id):
#     con = requirement.objects.get(c_id=c_id)
#     Age_of_Application_years = con.Age_of_Application_years
#     Usage_Frequency_times_day = con.Usage_Frequency_times_day
#     Physical_Activity_Level = con.Physical_Activity_Level
#     Impact_Resistance = con.Impact_Resistance
#     Wear_Resistance = con.Wear_Resistance
#     Corrosion_Resistance = con.Corrosion_Resistance
#     Temperature_Resistance = con.Temperature_Resistance
#
#     dataset = pd.read_csv('D:\Projects\Biomimetic_Prosthetics\Bio Analysis Algo.csv')
#
#     # Use the data from the Django model
#     X = dataset[['Age_of_Application_years', 'Usage_Frequency_times_day', 'Physical_Activity_Level',
#                  'Impact_Resistance', 'Wear_Resistance', 'Corrosion_Resistance',
#                  'Temperature_Resistance']]
#     y = dataset['Integrity_Level']
#
#     # Split the data into training and testing sets
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
#
#     # Create a pipeline with Random Projection and Linear Regression
#     pipeline = make_pipeline(
#         StandardScaler(),
#         GaussianRandomProjection(n_components=10, random_state=42),
#         LinearRegression()
#     )
#
#     # Train the model
#     pipeline.fit(X_train, y_train)
#
#     # Create a DataFrame with input data for prediction
#     input_data = pd.DataFrame([[Age_of_Application_years, Usage_Frequency_times_day, Physical_Activity_Level,
#                                  Impact_Resistance, Wear_Resistance, Corrosion_Resistance,
#                                  Temperature_Resistance]],
#                                columns=['Age_of_Application_years', 'Usage_Frequency_times_day',
#                                         'Physical_Activity_Level', 'Impact_Resistance',
#                                         'Wear_Resistance', 'Corrosion_Resistance',
#                                         'Temperature_Resistance'])
#
#     # Make predictions using the trained model
#     predictions = pipeline.predict(input_data)
#     print(predictions)
#     p = float(predictions)
#     print(p)
#     pre = round(p,4)
#     print(pre)
#
#     csv_path = r'D:\Projects\Biomimetic_Prosthetics\Bio Analysis.csv'
#     df = pd.read_csv(csv_path)
#     data = requirement.objects.filter(c_id=c_id)
#     for _, row in df.iterrows():
#         try:
#             req = data.get(prosthetics_type=row['Application'])
#             req.Material_Composition = row['Material Composition']
#             req.Age_of_Application_years = row['Age of Application (years)']
#             req.Usage_Frequency_times_day = row['Usage Frequency (times/day)']
#             req.Physical_Activity_Level = row['Physical Activity Level (1-10)']
#             req.Impact_Resistance = row['Impact Resistance (1-10)']
#             req.Wear_Resistance = row['Wear Resistance (1-10)']
#             req.Integrity = row['Integrity (1-10)']
#             req.Weight=row['Weight']
#             req.Characteristics=row['Characteristics']
#             req.Corrosion_Resistance = row['Corrosion Resistance (1-10)']
#             req.Temperature_Resistance = row['Temperature Resistance (1-10)']
#             integrity_level = sum(weight * characteristic for weight, characteristic in zip(req.Weight, req.Characteristics))
#             req.Integrity_Level = round(integrity_level, 2)
#             req.save()
#         except requirement.DoesNotExist:
#             pass
#
#     d = registration.objects.get(c_id=c_id)
#     d.badone = True
#     d.status = "Bio-Analysis Done"
#     d.save()
#     data1 = requirement.objects.get(c_id=c_id)
#     data1.badone2 = True
#     data1.Integrity_Level_Pre=pre
#     data1.save()
#
#     subject = 'Confirmation of Successful Bio-Analysis Process Completion'
#     message = f'Hi {d.name},\nWe are pleased to inform you that the Bio-Analysis Process has been successfully completed. Your requirements will be satisfied shortly, and we appreciate your patience.\n\nThank you for choosing our services.'
#
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [d.email]
#
#     email = EmailMessage(
#         subject,
#         message,
#         email_from,
#         recipient_list,
#     )
#     email.send()
#
#     messages.info(request, f"Bio Analysis Progressed Successfully for {c_id}")
#     return render(request, "bioanalysis/bioanalysis.html", {'data': data})



from django.shortcuts import render
from django.contrib import messages
import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split  #scikit-learn
from django.conf import settings
from django.core.mail import EmailMessage

def bioanalysis_process(request, c_id):
    con = requirement.objects.get(c_id=c_id)
    Age_of_Application_years = con.Age_of_Application_years
    Usage_Frequency_times_day = con.Usage_Frequency_times_day
    Physical_Activity_Level = con.Physical_Activity_Level
    Impact_Resistance = con.Impact_Resistance
    Wear_Resistance = con.Wear_Resistance
    Corrosion_Resistance = con.Corrosion_Resistance
    Temperature_Resistance = con.Temperature_Resistance

    dataset = pd.read_csv('D:\Project_PG\Biomimetic_Prosthetics\Bio Analysis Algo.csv')

    # Use the data from the Django model
    X = dataset[['Age_of_Application_years', 'Usage_Frequency_times_day', 'Physical_Activity_Level',
                 'Impact_Resistance', 'Wear_Resistance', 'Corrosion_Resistance',
                 'Temperature_Resistance']]
    y = dataset['Integrity_Level']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Create a pipeline with HistGradientBoostingRegressor
    model = HistGradientBoostingRegressor()

    # Train the model
    model.fit(X_train, y_train)

    # Create a DataFrame with input data for prediction
    input_data = pd.DataFrame([[Age_of_Application_years, Usage_Frequency_times_day, Physical_Activity_Level,
                                 Impact_Resistance, Wear_Resistance, Corrosion_Resistance,
                                 Temperature_Resistance]],
                               columns=['Age_of_Application_years', 'Usage_Frequency_times_day',
                                        'Physical_Activity_Level', 'Impact_Resistance',
                                        'Wear_Resistance', 'Corrosion_Resistance',
                                        'Temperature_Resistance'])

    # Make predictions using the trained model
    predictions = model.predict(input_data)
    pre = round(float(predictions), 4)

    data = requirement.objects.get(c_id=c_id)
    csv_path = r'D:\Project_PG\Biomimetic_Prosthetics\Bio Analysis.csv'
    df = pd.read_csv(csv_path)
    for index, row in df.iterrows():
        if data.prosthetics_type == row['Applications']:
            data.Material_Composition = row['Material Composition']
            data.Age_of_Application_years = row['Age of Application (years)']
            data.Usage_Frequency_times_day = row['Usage Frequency (times/day)']
            data.Physical_Activity_Level = row['Physical Activity Level (1-10)']
            data.Impact_Resistance = row['Impact Resistance (1-10)']
            data.Wear_Resistance = row['Wear Resistance (1-10)']
            data.Integrity = row['Integrity (1-10)']
            data.Weight = row['Weight']
            data.Characteristics = row['Characteristics']
            data.Corrosion_Resistance = row['Corrosion Resistance (1-10)']
            data.Temperature_Resistance = row['Temperature Resistance (1-10)']

            # integrity_level = sum(
            #     weight * characteristic for weight, characteristic in zip(data.Weight, data.Characteristics))
            # data.Integrity_Level = round(integrity_level, 2)

            data.save()

    d = registration.objects.get(c_id=c_id)
    d.badone = True
    d.status = "Bio-Analysis Done"
    d.save()
    data1 = requirement.objects.get(c_id=c_id)
    data1.badone2 = True
    data1.Integrity_Level_Pre=pre
    data1.save()

    subject = 'Confirmation of Successful Bio-Analysis Process Completion'
    message = f'Hi {d.name},\nWe are pleased to inform you that the Bio-Analysis Process has been successfully completed. Your requirements will be satisfied shortly, and we appreciate your patience.\n\nThank you for choosing our services.'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [d.email]

    email = EmailMessage(
        subject,
        message,
        email_from,
        recipient_list,
    )
    email.send()
    messages.info(request, f"Bio Analysis Progressed Successfully for {c_id}")
    return render(request, "bioanalysis/bioanalysis.html", {'con': data})




#Bioanalysis Report
def bioanalysis_report(request):
    data=requirement.objects.filter(badone2=True)
    return render(request,"bioanalysis/bioanalysis_report.html",{'data':data})