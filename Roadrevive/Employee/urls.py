from django.urls import path

from Employee import views




app_name = 'Employee'

urlpatterns = [
        path('Employee_home/', views.Employee_home, name='Employee_home'),
        path('employee_register/', views.employee_register, name='employee-register'),
        path('assigned-jobs/', views.assigned_jobs, name='assigned_jobs'),
        path('accept-job/<int:complaint_id>/', views.accept_job, name='accept_job'),
        path('complete-job/<int:complaint_id>/', views.complete_job, name='complete_job'),
        path('profile/', views.employee_profile, name='employee_profile'),
        path('profile/edit/', views.edit_employee_profile, name='edit_employee_profile'),
        path('profile/change-password/', views.change_employee_password, name='change_employee_password'),
]