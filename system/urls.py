from django.urls import path
from . import views

urlpatterns = [
    path('signup-admin/', views.signup_admin, name='signup_admin'),
    path('signin-admin/', views.signin_admin, name='signin_admin'),
    path('home/', views.home, name='home' ),
    path('student-home/', views.student_home, name='student_home' ),
    path('accounts/login/', views.home, name='home' ),
    path('logout/', views.logout, name='logout'),

    path('add-student/', views.add_student, name='add_student' ),
    path('view-student/', views.view_students, name='view_students' ),
    path('delete/<student_id>/', views.delete_student, name='delete_student' ),
    path('edit/<student_id>/', views.edit_student, name='edit_student' ),

    path('add-teacher/', views.add_teacher, name='add_teacher' ),
    path('view-teacher/', views.view_teachers, name='view_teachers' ),
    path('deletet/<teacher_id>/', views.delete_teacher, name='delete_teacher' ),
    path('editt/<teacher_id>/', views.edit_teacher, name='edit_teacher' ),

    path('add-department/', views.add_department, name='add_department' ),
    path('view-department/', views.view_departments, name='view_departments' ),
    path('deleted/<department_id>/', views.delete_department, name='delete_department' ),

    path('v-student/', views.v_students, name='v_students' ),
    path('v-teacher/', views.v_teachers, name='v_teachers' ),
    path('v-department/', views.v_departments, name='v_departments' ),
]
