from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib import messages
from Department.models import Department
from Employee.models import Employee
from User.models import Complaint

# Create your views here.


def Department_home(request):
    return render(request,'Department/Dept_home.html')

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



def department_complaints(request):
    if not request.session.get('Did'):  
        messages.error(request, "You need to be logged in to view complaints.")
        return redirect('Department:Department_home')  

    complaints = Complaint.objects.all() 
    employees = Employee.objects.all()  

    context = {
        'complaints': complaints,
        'employees': employees,
    }
    return render(request, 'Department/department_complaints.html', context)

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


def assign_employee(request, complaint_id):
    if request.method == "POST":
        employee_id = request.POST.get('employee_id')  
        print(f"Received employee ID: {employee_id}")  

        try:
            complaint = Complaint.objects.get(id=complaint_id)
            complaint.employee_id = employee_id  
            complaint.status = 'In Progress'  
            complaint.save()
            messages.success(request, "Employee assigned and complaint status updated to In Progress.")
            return redirect('Department:department-complaints')
        except Complaint.DoesNotExist:
            messages.error(request, "Complaint not found.")
    
    employees = Employee.objects.all()
    complaint = Complaint.objects.get(id=complaint_id) 
    return render(request, 'Department/assign_employee.html', {'employees': employees, 'complaint': complaint})

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def update_password(request):
    did = request.session.get('Did')
    if not did:
        messages.error(request, 'You are not authorized to update the password.')
        return redirect('Department:Department_home')  
    if request.method == 'POST':
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        department_user = get_object_or_404(Department, id=did)

        if current_password == department_user.password:  
            if new_password == confirm_password:
                department_user.password = new_password  
                department_user.save()
                messages.success(request, 'Password updated successfully!')
                return redirect('Department:Department_home')
            else:
                messages.error(request, 'New passwords do not match.')
        else:
            messages.error(request, 'Current password is incorrect.')

    return render(request, 'Department/update_password.html')