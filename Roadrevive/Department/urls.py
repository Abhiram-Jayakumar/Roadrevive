from django.urls import path

from Department import views




app_name = 'Department'

urlpatterns = [
        path('Department_home/', views.Department_home, name='Department_home'),
        path('complaints/', views.department_complaints, name='department-complaints'),
        path('assign-employee/<int:complaint_id>/',views. assign_employee, name='assign-employee'),
        path('update_password/',views. update_password, name='update_password'),
]