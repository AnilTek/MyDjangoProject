from faulthandler import disable
from sqlite3 import IntegrityError
from django.shortcuts import  render,redirect
import numpy as np
from .forms import CarForm,LoanForm
from joblib import load
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from django.db import transaction
from django.contrib.auth import get_user_model
from django.contrib import messages

car_model_predict = load('./savedModels/carmodel.joblib')
loan_model_predict = load('./savedModels/LoanapprovalModel.joblib')

# Create your views here.

pets = [
  { "petname": "Fido", "animal_type": "dog"},
  { "petname": "Clementine", "animal_type": "cat"},
  { "petname": "Cleo", "animal_type": "cat"},
  { "petname": "Oreo", "animal_type": "dog"},
]

def home(request):
# BOS 
     return render(request,'home.html')

def about(request):
    
    result = 1
    
    context = {
         "name":"Anil",
         "pets": pets,
         "result": 1 ,
    } 
     
    return render(request,'about.html',context=context)

def cars(request):
     return render(request,'cars.html')
def contact(request):
     return render(request,'contact.html')
def houses(request):
     return render(request,'houses.html')


##LOGIN ----------------------------------------------------------------------------------
def login_request(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            return redirect('home')  
        else:
            
            return render(request, 'login.html', {'error_message': 'Invalid credentials'})  
     else:
        return render(request, 'login.html')
##LOGIN-----------------------------------------------------------------------------------


##LOGOUT----------------------------------------------------------------------------------
def logout_request(request):
    logout(request)
    return redirect('login_request')
##LOGOUT----------------------------------------------------------------------------------


CustomUser = get_user_model()

def signup_request(request):
    if request.method == 'POST':
        try:
            with transaction.atomic():
                name = request.POST["name"]
                surname = request.POST["surname"]
                email = request.POST['email']
                username = request.POST['username']
                password = request.POST['password']
                repassword = request.POST['repassword']
                gender = request.POST['gender']
                sec_question = request.POST['sec_question']
                sec_answer = request.POST['sec_answer']

                sec_question_answer = None

                if sec_question == 'q1':
                    sec_question_answer='Name of your first pet ?'
                elif sec_question == 'q2':
                    sec_question_answer = "Name of your favorite food ?"
                else :
                    sec_question_answer = "What is your lucky Number ?"
 
               
                if password != repassword:
                    return render(request, 'signup.html', {'error': 'Passwords do not match!'})

                
                if CustomUser.objects.filter(username=username).exists():
                    return render(request, "signup.html", {'error': "Username already exists!"})
                elif CustomUser.objects.filter(email=email).exists():
                    return render(request, "signup.html", {'error': "This email already has an account"})

                
                user = CustomUser(
                    name=name,
                    surname=surname,
                    email=email,
                    gender=gender,
                    sec_question=sec_question_answer,
                    sec_answer=sec_answer,
                    username=username
                )
                
                user.set_password(password)
                user.save()

                return redirect('login_request')

        except IntegrityError:
            return render(request, 'signup.html', {'error': 'Database error occurred!'})
 
    else:
        return render(request, 'signup.html')




def resetpassword_request(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        user = CustomUser.objects.filter(username=username).first()

        if user:
            sec_question = user.sec_question  
            sec_answer = request.POST.get('sec_answer')

            if sec_answer == user.sec_answer:
                return render(request, 'resetpassword.html', {'username_entered': True, 'sec_question': sec_question, 'sec_answer_matched': True})
            else:
                error = "Güvenlik sorusu yanlış. Lütfen tekrar deneyin."
        else:
            error = "Kullanıcı bulunamadı. Lütfen doğru bir kullanıcı adı girin."
            return render(request, 'resetpassword.html', {'error': error})

    return render(request, 'resetpassword.html')



   

    


## CAR SALE --------------------------------------------------------------------------------------
def carmodel(request):
    if request.method == 'POST':
        form = CarForm(request.POST)
        if form.is_valid():
            model = form.cleaned_data.get('model', 0)
            year = form.cleaned_data.get('year', 0)
            millage = form.cleaned_data.get('millage', 0)
            tax = form.cleaned_data.get('tax', 0)
            mpg = form.cleaned_data.get('mpg', 0)
            engineSize = form.cleaned_data.get('engineSize', 0)
            transmission = int(request.POST.get('transmission', 0))
            fuel = int(request.POST.get('fuel', 0))

            transmission_Automatic = transmission_Manual = transmission_Semi = 0
            fuel_Diesel = fuel_Electric = fuel_Hybrid = fuel_Other = fuel_Petrol = 0

            if transmission == 0:
                transmission_Automatic = 1
            elif transmission == 1:
                transmission_Manual = 1
            elif transmission == 2:
                transmission_Semi = 1

            if fuel == 0:
                fuel_Diesel = 1
            elif fuel == 1:
                fuel_Electric = 1
            elif fuel == 2:
                fuel_Hybrid = 1
            elif fuel == 3:
                fuel_Other = 1
            elif fuel == 4:
                fuel_Petrol = 1
            else:
                print('There is something wrong with the form')
             


            prediction = car_model_predict.predict([[year,millage,tax,mpg,engineSize,transmission_Automatic,transmission_Manual,transmission_Semi,fuel_Diesel,fuel_Electric,fuel_Hybrid,fuel_Other,fuel_Petrol]])

            context = {
                'context':prediction[0]
            }
            

            print(f'Arabanin Yakit tipi dizel: {fuel_Diesel}, elektrik: {fuel_Electric}, hybrid: {fuel_Hybrid}, other: {fuel_Other}, petrol: {fuel_Petrol},')
            print(f'Arabanin sanziman tipi otomatik:{transmission_Automatic} , manuel:{transmission_Manual} , semi-otomatik:{transmission_Semi}')
            print(f'Model :{model} , year :{year} , millage :{millage} , mpg :{mpg} , engineSize :{engineSize} , tax :{tax}  ')
            return render(request, 'carmodel.html', context=context)
    else:
        form = CarForm()

    return render(request, 'carmodel.html',context={'context':'Please Enter Valid Values'})
#CAR SALE ------------------------------------------------------------------------------------------



#BANK LOAN REQUEST -----------------------------------------------------------------------------------
def loanmodel(request):
      if request.method == 'POST':
        form = LoanForm(request.POST)
        if form.is_valid():
            number_of_dependents = form.cleaned_data.get('number_of_dependents', 0)
            anual_income = form.cleaned_data.get('anual_income', 0)
            loan_ammount = form.cleaned_data.get('loan_ammount', 0)
            loan_term = form.cleaned_data.get('loan_term', 0)
            cibil_score = form.cleaned_data.get('cibil_score', 0)
            residental_assets_value = form.cleaned_data.get('residental_assets_value', 0)
            commercial_assets_value = form.cleaned_data.get('commercial_assets_value', 0)
            luxury_assets_value = form.cleaned_data.get('luxury_assets_value', 0)
            bank_asset_value = form.cleaned_data.get('bank_asset_value', 0)
            graduate = int(request.POST.get('graduate', 0))
            employed = int(request.POST.get('employed', 0))
             


            prediction = loan_model_predict.predict([[number_of_dependents,anual_income,loan_ammount,loan_term,cibil_score,residental_assets_value,commercial_assets_value,luxury_assets_value,bank_asset_value,graduate,employed]])

            context = {
                'context':prediction[0]
            }
            
            return render(request, 'loanmodel.html', context=context)
      else:
        form = CarForm()

    
      return render(request,'loanmodel.html')
#BANK LOAN REQUEST -----------------------------------------------------------------------------------






         
