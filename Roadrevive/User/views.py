from django.shortcuts import redirect, render
from django.contrib import messages

from Department.models import Department
from Employee.models import Employee
from User.models import Complaint, User
# Create your views here.


def login(request):
    if request.method=="POST":
        email=request.POST.get('email')
        password=request.POST.get('password')
        Deptlogin=Department.objects.filter(email=email,password=password).count()
        Userlogin=User.objects.filter(email=email,password=password).count()
        Emplogin=Employee.objects.filter(email=email,password=password).count()


        if Deptlogin > 0:
            Deptadmin=Department.objects.get(email=email,password=password)
            request.session['Did']=Deptadmin.id
            return redirect('Department:Department_home')
        elif Userlogin > 0:
            Useradmin=User.objects.get(email=email,password=password)
            request.session['Uid']=Useradmin.id
            return redirect('User:User_home')
        elif Emplogin > 0:
            Empadmin=Employee.objects.get(email=email,password=password)
            request.session['Eid']=Empadmin.id
            return redirect('Employee:Employee_home')
        
        else:
            error="Invalid Credentials!!"
            return render(request,"User/login.html",{'ERR':error})
    else:
        return render(request, "User/login.html")
    



#///////////////////////////////////////////////////////////////////////////////////////////////////


def User_home(request):
    return render(request,'User/user_home.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////


def index(request):
    return render(request,'User/index.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////


def User_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        id_number = request.POST.get('id_number')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'User/register_user.html')

        if User.objects.filter(id_number=id_number).exists():
            messages.error(request, "ID number already registered.")
            return render(request, 'User/register_user.html')

        user = User(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            id_number=id_number,
            password=password  
        )
        user.save()

        messages.success(request, "Registration successful. You can now log in.")
        return redirect('User:index')

    return render(request, 'User/register_user.html')

#///////////////////////////////////////////////////////////////////////////////////////////////////

def file_complaint(request):
    if request.method == "POST":
        user_id = request.session.get('Uid')   
        category = request.POST.get('category')
        description = request.POST.get('description')
        location = request.POST.get('location')
        pin = request.POST.get('pin')
        landmark = request.POST.get('landmark')
        image = request.FILES.get('image') 

        if not user_id:
            messages.error(request, "You need to be logged in to file a complaint.")
            return redirect('User:User_home')  
        complaint = Complaint(
            user_id=user_id,  
            category=category,
            description=description,
            image=image,
            pin=pin,
            landmark=landmark,
            location=location
        )
        complaint.save()

        messages.success(request, "Your complaint has been filed successfully.")
        return redirect('User:User_home') 

    return render(request, 'User/file_complaint.html')


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def user_complaints(request):
    if not request.session.get('Uid'):  
        messages.error(request, "You need to be logged in to view your complaints.")
        return redirect('User:User_home')  

    user_id = request.session['Uid']
    complaints = Complaint.objects.filter(user_id=user_id) 

    context = {
        'complaints': complaints,
    }
    return render(request, 'User/user_complaints.html', context)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def submit_feedback(request, complaint_id):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        
        try:
            complaint = Complaint.objects.get(id=complaint_id)

            if complaint.status == 'Resolved':  
                complaint.feedback = feedback
                complaint.save()
                messages.success(request, "Feedback submitted successfully.")
            else:
                messages.error(request, "Feedback can only be submitted for resolved complaints.")
            
        except Complaint.DoesNotExist:
            messages.error(request, "Complaint not found.")
    
    return redirect('User:user-complaints')


#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def user_profile(request):
    if not request.session.get('Uid'):
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect('User:login')  
    
    try:
        user = User.objects.get(id=request.session['Uid'])
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('User:login')

    context = {
        'user': user,
    }
    return render(request, 'User/user_profile.html', context)

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def edit_profile(request):
    if not request.session.get('Uid'):
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('User:login')

    user = User.objects.get(id=request.session['Uid'])

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        user.name = name
        user.email = email
        user.phone_number = phone_number
        user.address = address
        user.save()

        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('User:profile')

    return render(request, 'User/edit_profile.html', {'user': user})


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def change_password(request):
    if not request.session.get('Uid'):
        messages.error(request, "You need to be logged in to change your password.")
        return redirect('User:login')

    user = User.objects.get(id=request.session['Uid'])

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if current_password != user.password:
            messages.error(request, "Current password is incorrect.")
            return redirect('User:change_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('User:change_password')

        user.password = new_password
        user.save()

        messages.success(request, "Password updated successfully.")
        return redirect('User:profile')

    return render(request, 'User/change_password.html')