from django.shortcuts import redirect, render
from django.contrib import messages

from Employee.models import Employee
from User.models import Complaint

# Create your views here.

def Employee_home(request):
    return render(request,'Employee/Emp_home.html')

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def employee_register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        position = request.POST.get('position')
        date_of_birth = request.POST.get('date_of_birth')
        password = request.POST.get('password')

        if Employee.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'Employee/employee_register.html')

        employee = Employee(
            name=name,
            email=email,
            phone_number=phone_number,
            address=address,
            position=position,
            date_of_birth=date_of_birth,
            password=password 
        )
        employee.save()

        messages.success(request, "Employee registered successfully.")
        return redirect('Employee:employee-register')

    return render(request, 'Employee/employee_register.html')

#/////////////////////////////////////////////////////////////////////////////////////////////////////


def assigned_jobs(request):
    if not request.session.get('Eid'): 
        messages.error(request, "You need to be logged in to view your assigned jobs.")
        return redirect('Employee:Employee_home')  

    employee_id = request.session['Eid']
    assigned_complaints = Complaint.objects.filter(employee_id=employee_id)

    context = {
        'assigned_complaints': assigned_complaints,
    }
    return render(request, 'Employee/assigned_jobs.html', context)


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def accept_job(request, complaint_id):
    if not request.session.get('Eid'):
        messages.error(request, "You need to be logged in to accept jobs.")
        return redirect('Employee:Employee_home')

    try:
        complaint = Complaint.objects.get(id=complaint_id)
        
        complaint.status = 'Work agreed'
        complaint.save()

        messages.success(request, "Job accepted successfully.")
        return redirect('Employee:assigned_jobs')  
    except Complaint.DoesNotExist:
        messages.error(request, "Complaint not found.")
        return redirect('Employee:assigned_jobs') 
    
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def complete_job(request, complaint_id):
    if not request.session.get('Eid'):
        messages.error(request, "You need to be logged in to complete jobs.")
        return redirect('Employee:Employee_home')

    try:
        complaint = Complaint.objects.get(id=complaint_id)
        complaint.status = 'Resolved'  
        complaint.save()
        messages.success(request, "Job marked as completed successfully.")
        return redirect('Employee:assigned_jobs')

    except Complaint.DoesNotExist:
        messages.error(request, "Complaint not found.")
        return redirect('Employee:assigned_jobs')
    

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////


def employee_profile(request):
    if not request.session.get('Eid'):  
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect('Employee:login')

    employee = Employee.objects.get(id=request.session['Eid'])
    context = {'employee': employee}
    return render(request, 'Employee/employee_profile.html', context)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



def edit_employee_profile(request):
    if not request.session.get('Eid'):
        messages.error(request, "You need to be logged in to edit your profile.")
        return redirect('Employee:login')

    employee = Employee.objects.get(id=request.session['Eid'])

    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.phone_number = request.POST.get('phone_number')
        employee.address = request.POST.get('address')
        employee.position = request.POST.get('position')
        employee.date_of_birth = request.POST.get('date_of_birth')
        
        employee.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('Employee:employee_profile')

    context = {'employee': employee}
    return render(request, 'Employee/edit_employee_profile.html', context)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def change_employee_password(request):
    if not request.session.get('Eid'):
        messages.error(request, "You need to be logged in to change your password.")
        return redirect('Employee:login')

    employee = Employee.objects.get(id=request.session['Eid'])

    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if current_password != employee.password:
            messages.error(request, "Current password is incorrect.")
            return redirect('Employee:change_employee_password')

        if new_password != confirm_password:
            messages.error(request, "New passwords do not match.")
            return redirect('Employee:change_employee_password')

        employee.password = new_password
        employee.save()

        messages.success(request, "Password updated successfully.")
        return redirect('Employee:employee_profile')

    return render(request, 'Employee/change_employee_password.html')
