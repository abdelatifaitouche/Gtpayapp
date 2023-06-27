from django.shortcuts import render , redirect
from .models import * 
from django.contrib.auth import authenticate , login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import * 
from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserCreationForm

from .decorators import *

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.


@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def home(request):
    employee = Employee.objects.all()
    files = Files.objects.all().order_by("-created_at")
    nbr_employee = len(employee)
    context = {'nombre' : nbr_employee , 'fiche_de_paie' : files}
    return render(request , 'app/dashboard.html' , context)


@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def employee(request):
    employee = Employee.objects.all()
    nbr_employee = len(employee)
    context = {'employee' : employee , 'nombre' : nbr_employee}
    return render(request , 'app/employe.html' , context)






@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def employee_details(request , pk):
    employee = Employee.objects.get(id = pk)
    context = {'employee' : employee}
    return render(request , 'app/employee_details.html' , context)


@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def upload_file(request):
    if request.method =='POST' :
        data = request.POST
        files = request.FILES.getlist('file')
        for file in files :
            instance = Files.objects.create(fiche=file)
    context = {}
    return render(request , 'app/upload.html' , context)



def loginPage(request):
    if request.method == "POST" :
        username = request.POST.get('username')
        password = request.POST.get('password')


        user = authenticate(request , username = username , password=password)
        if user is not None :
            login(request , user)
            if user.is_staff:
                return redirect('dashboard')
            else : 
                return redirect('user_page')
        else :
            messages.info(request , 'please check your informations')


    return render(request , 'app/login.html')


@login_required(login_url='loginpage')
def logoutuser(request):
    logout(request)
    return redirect('loginpage')


@login_required(login_url='loginpage')
def userPage(request):
    current_user = request.user.employee
    matricule = current_user.matricule
    files = Files.objects.filter(fiche__startswith= matricule).order_by("-created_at")
    
    context = {'files' : files}
   
    


    #context = {'files' : files , 'user' : current_user}
    return render(request , 'app/user_page.html' , context)

@login_required(login_url='loginpage')
def download_file(request , pk):
    obj = Files.objects.get(id=pk)
    response = HttpResponse(obj.fiche, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{obj.fiche.name}"'
    return response



@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def create_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            group = Group.objects.get(name = 'employee')
            Employee.objects.create(user = user , name = user.username , matricule = form.cleaned_data['matricule'] , email=form.cleaned_data['email'])
            user.groups.add(group)
            return redirect('create_user')
    context = {'form' : form}

    return render(request , 'app/create_user.html' , context)



@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def updateUser(request , pk):
    employee = Employee.objects.get(id=pk)
    user = User.objects.get(username = employee.user.username)
    user_form = CreateUserForm(instance = user)
    employee_form = CreateUserForm(instance = employee)

    if request.method=="POST":
        user_form = CreateUserForm(request.POST , instance = user)
        employee_form = CreateUserForm(request.POST , instance = employee)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save()
            employee = employee_form.save()
            return redirect('employee')
    context = {'user_form':user_form ,'employee_form' : employee_form ,  'employee' : employee}
    return render(request , 'app/employe_form.html',context)




@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['admin' , 'staff'])
def deleteUser(request , pk):
    employee = Employee.objects.get(id=pk)
    user = User.objects.get(username = employee.name)
    if request.method == "POST" :
        employee.delete()
        user.delete()
        return redirect('employee')
    context = {'employee' : employee}
    return render(request , 'app/delete_employee.html' , context)



@login_required(login_url='loginpage')
@allowed_user(allowed_roles=['employee'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/change_password.html', {
        'form': form
    })
