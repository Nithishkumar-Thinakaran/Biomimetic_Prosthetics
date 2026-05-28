from django.db import models

# Create your models here.
class registration(models.Model):
    name=models.CharField(max_length=50)
    phone = models.PositiveBigIntegerField()
    email=models.EmailField(unique=True,max_length=50,null=True)
    password=models.CharField(max_length=50)
    status = models.CharField(max_length=50,null=True,default="Pending")

    approve = models.BooleanField(null=True, default=False)
    reject = models.BooleanField(null=True, default=False)
    c_id = models.CharField(null=True, max_length=50)

    login = models.BooleanField(null=True, default=False)
    logout = models.BooleanField(null=True, default=False)

    ihdone= models.BooleanField(null=True, default=False)
    badone = models.BooleanField(null=True, default=False)
    abdone= models.BooleanField(null=True, default=False)

    final= models.BooleanField(null=True, default=False)

class requirement(models.Model):
    c_id = models.CharField(null=True, max_length=50)
    name = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    age= models.PositiveBigIntegerField(null=True)
    height= models.PositiveBigIntegerField(null=True)
    width= models.PositiveBigIntegerField(null=True)
    medical_condition=models.CharField(max_length=50)
    prosthetics_type=models.CharField(max_length=50)

    #Integration Process(IntegrateHub)

    Integrate_Hub_Report = models.FileField(upload_to='Integrate_Hub_Report/', null=True)

    ihdone1= models.BooleanField(null=True, default=False)

    #Bio Analysis
    Material_Composition=models.CharField(max_length=50,null=True)
    Age_of_Application_years= models.PositiveBigIntegerField(null=True)
    Usage_Frequency_times_day= models.PositiveBigIntegerField(null=True)
    Physical_Activity_Level= models.PositiveBigIntegerField(null=True)
    Impact_Resistance= models.PositiveBigIntegerField(null=True)
    Wear_Resistance= models.PositiveBigIntegerField(null=True)
    Corrosion_Resistance= models.PositiveBigIntegerField(null=True)
    Temperature_Resistance= models.PositiveBigIntegerField(null=True)
    Integrity= models.PositiveBigIntegerField(null=True)
    Weight= models.CharField(max_length=50,null=True)
    Characteristics = models.CharField(max_length=50,null=True)
    # Integrity_Level=models.FloatField(null=True)
    Integrity_Level_Pre=models.FloatField(null=True)

    badone2=models.BooleanField(null=True, default=False)

    #Actu-Bio
    Actuation_Mechanism=models.CharField(max_length=250,null=True)
    Biocompatibility_Factors=models.CharField(max_length=250,null=True)
    Typical_Force_Output_N=models.CharField(max_length=250,null=True)
    Specific_Surface_Area=models.CharField(max_length=250,null=True)
    Control_Response_Time=models.CharField(max_length=250,null=True)
    Energy_Density=models.CharField(max_length=250,null=True)
    Weight_Actubio=models.CharField(max_length=250,null=True)

    abdone3=models.BooleanField(null=True, default=False)

    bp_final_report= models.FileField(upload_to='BP_Final_Report/', null=True)

    finalreportview = models.BooleanField(null=True, default=False)

    finalreportapprove=models.BooleanField(null=True, default=False)
    finalreportreject=models.BooleanField(null=True, default=False)


