from django.urls import path

from User import views




app_name = 'User'

urlpatterns = [
        path('index/', views.index, name='index'),
        path('login/', views.login, name='login'),
        path('User_home/', views.User_home, name='User_home'),
        path('User_register/', views.User_register, name='User_register'),
        path('file-complaint/', views.file_complaint, name='file-complaint'),
        path('your-complaints/',views.user_complaints, name='user-complaints'),
        path('submit-feedback/<int:complaint_id>/', views.submit_feedback, name='submit_feedback'), 
        path('profile/', views.user_profile, name='profile'),
        path('profile/edit/', views.edit_profile, name='edit_profile'),
        path('profile/change-password/', views.change_password, name='change_password'),
]