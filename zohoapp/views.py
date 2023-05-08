from django.shortcuts import render,redirect
from django.contrib import messages
from django.utils.text import capfirst
from django.contrib.auth.models import User,auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login




def index(request):

    return render(request,'index.html')

def register(request):
    if request.method=='POST':

        first_name=capfirst(request.POST['fname'])
        last_name=capfirst(request.POST['lname'])
        username=request.POST['uname']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        email=request.POST['email1']
        phone = request.POST['phone']

      
        if password==cpassword:  #  password matching......
            if User.objects.filter(username=username).exists(): #check Username Already Exists..
                messages.info(request, 'This username already exists!!!!!!')
                return redirect('register')
            else:
                user=User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)
                
                user.save()
                u = User.objects.get(id = user.id)

                company_details(contact_number = phone, user = u).save()
        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ") 
            return redirect('register')   
        return redirect('register')

    return render(request,'register.html',{'msg' : messages})

def login(request):
        
    if request.method == 'POST':
        
        email_or_username = request.POST['emailorusername']
        password = request.POST['password']

        user = authenticate(request, username=email_or_username, password=password)
        # print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('base')
        else:
            return redirect('/')

    return render(request, 'register.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')

@login_required(login_url='login')
def base(request):

    company = company_details.objects.get(user = request.user)
    context = {
                'company' : company
            }
    return render(request,'base.html',context)

@login_required(login_url='login')
def view_profile(request):

    company = company_details.objects.get(user = request.user)
    context = {
                'company' : company
            }
    return render(request,'profile.html',context)

@login_required(login_url='login')
def edit_profile(request,pk):

    company = company_details.objects.get(id = pk)
    user1 = User.objects.get(id = company.user_id)

    if request.method == "POST":

        user1.first_name = capfirst(request.POST.get('f_name'))
        user1.last_name  = capfirst(request.POST.get('l_name'))
        user1.email = request.POST.get('email')
        company.contact_number = request.POST.get('cnum')
        company.address = capfirst(request.POST.get('ards'))
        company.company_name = request.POST.get('comp_name')
        company.company_email = request.POST.get('comp_email')
        company.city = request.POST.get('city')
        company.state = request.POST.get('state')
        company.pincode = request.POST.get('pinc')
        company.business_name = request.POST.get('bname')
        company.company_type = request.POST.get('comp_type')
        if len(request.FILES)!=0 :
            company.profile_pic = request.FILES.get('file')

        company.save()
        user1.save()
        return redirect('view_profile')

    context = {
        'company' : company,
        'user1' : user1,
    }
    
    return render(request,'edit_profile.html',context)