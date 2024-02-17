from django.shortcuts import render,redirect
from .forms import CreateUserForm,LoginForm,CreateRecordForm,UpdateRecordForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login

from django.contrib.auth.decorators import login_required

from .models import Record
from django.contrib import messages


# Create your views here.



def home(request):
    # return HttpResponse("Hello Home!")
    return render(request,'app/index.html')

# -->REGISTER 

def register(request):
    form = CreateUserForm()
    
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success(request,"Account created successfully!")
            return redirect("my-login")
    
    context = {'form': form}
    
    return render(request, 'app/register.html', context=context)


# -->LOGIN

def my_login(request):
    form = LoginForm()
    
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid(): #is_valid checks the required fields,fields type and more.
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                
                return redirect('dashboard')  # Assuming you have a URL named 'dashboard' defined in your urls.py

    context = {'form':form}

    return render(request, 'app/my-login.html', context=context)



# -->LOGOUT

def user_logout(request):
    
    auth.logout(request)
    
    messages.success(request,"Logout successfully!")
    
    return redirect('my-login')

# --> DASHBOARD/HOME
@login_required(login_url='my-login')
def dashboard(request):
    
    my_records = Record.objects.all()
    
    context = {'records':my_records}
    
    
    return render(request,'app/dashboard.html', context=context)

# -->ADDING A RECORD
@login_required(login_url='my-login')
def create_record(request):
    
    form = CreateRecordForm()
    
    
    if request.method == "POST":
        
        form = CreateRecordForm(request.POST,request.FILES)
        
        if form.is_valid():
            
            form.save()
            
            messages.success(request,"Record created successfully!")
            
            return redirect('dashboard')
        
    context = {'form':form}
    
    return render(request,'app/create-record.html',context=context)



# -->UPDATE RECORD
@login_required(login_url='my-login')
def update_record(request,pk):
    record = Record.objects.get(id=pk)
    
    form = UpdateRecordForm(instance=record)
    
    if request.method =="POST":
        form = UpdateRecordForm(request.POST, request.FILES,instance=record)
        if form.is_valid():
            form.save()
            
            messages.success(request,"Record updated successfully!")
            
            return redirect('dashboard')
        
    context = {'form': form}   
    
    return render(request,'app/update-record.html',context=context)

# --> View a record
@login_required(login_url='my-login')
def see_record(request,pk):
    
    all_records = Record.objects.get(id=pk)
    
    context = {'record':all_records}
    
    return render(request,'app/view-record.html',context=context)


# -->DELETE 

@login_required(login_url='my-login')
def delete_record(request,pk):
    
    record = Record.objects.get(id=pk)
    
    record.delete()
    
    messages.success(request,"Record was deleted!")
    
    return redirect('dashboard')