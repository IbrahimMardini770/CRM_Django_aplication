from django.shortcuts import render , redirect , HttpResponse

from . forms import CreateUserForm , LoginForm , CreateRecordForm , UpdateRecordForm

from django.contrib.auth.models import auth # this will allow the user to logout or login

from django.contrib.auth import authenticate # هذه ستقوم بموافقة اسم المستخدم و كلمة السر

from django.contrib.auth.decorators import login_required # to makee login required

from .models import Record

from django.contrib import messages  #

# - Home page------------------

def home(request):
    # return HttpResponse("hi")
    return render(request , 'webapp/index.html')

# - Register --------------------

def register(request):

    form = CreateUserForm()

    if request.method == "POST":

        form = CreateUserForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(request , "Account created successsfully!")

            return redirect("my-login")

    context = {'form':form}
    
    return render(request, 'webapp/register.html', context=context)


# - Login a user ------------------------

def my_login(request):
    
    form = LoginForm()

    if request.method == "POST":
        
        form = LoginForm(request , data = request.POST)
        
        if form.is_valid():
            
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            user = authenticate(request , username = username , password = password)
            
            if user is not None:
                
                auth.login(request , user)

                return redirect('dashboard')

    context = {'form' : form}
    return render(request , 'webapp/my-login.html' , context = context)

# - Logout ------------------------------------

def user_logout(request):
    
    auth.logout(request)

    messages.success(request , "Logout success!")

    return redirect("my-login")

# - Dashboard --------------------------------

@login_required(login_url='my-login')
def dashboard(request):

    my_records = Record.objects.all()

    context = {'records': my_records}

    return render(request, 'webapp/dashboard.html', context=context)

# - Create a record

@login_required(login_url='my-login')
def create_record(request):
    
    form = CreateRecordForm()

    if request.method == 'POST':
        
        form = CreateRecordForm(request.POST)

        if form.is_valid():
            form.save()
            
            messages.success(request , "Your record was createdk!")
            
            return redirect("dashboard")
        

    context = {'form' : form}            

    return render(request , 'webapp/create-record.html' , context = context )

# - update a record

@login_required(login_url='my-login')
def update_record(request , pk):
    
    record = Record.objects.get(id = pk)

    form = UpdateRecordForm(instance=record) 
    #هذا لكي يحضر بيانات الذي في قاعدة البيانات ثم يتحقق من وجودها في السطر القادم 
    
    if request.method == "POST":
        
        form = UpdateRecordForm(request.POST , instance=record)
        
        if form.is_valid():
            
            form.save()
            
            messages.success(request , "Your record was updated!")
            
            return redirect("dashboard")
        
    context = {"form" : form}

    return render(request , 'webapp/update-record.html' , context=context)

# - Read / View a singular record

@login_required(login_url='my-login')
def singlur_record(request , pk):
    
    all_records = Record.objects.get(id =pk)
    
    context = {'record':all_records}

    return render(request , 'webapp/view-record.html' , context = context )


# - Delete  a record
@login_required(login_url='my-login')
def delete_rcord(request , pk):
    record = Record.objects.get(id=pk)

    messages.success(request , "Your record was deleted!")
    
    record.delete()

    return redirect("dashboard")

