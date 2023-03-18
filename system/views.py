from django.shortcuts import render, redirect
from django.db import connection
from .models import *
from django.contrib.auth import logout, login, authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse


def signup_admin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        # Check if user with given email already exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM Admin WHERE email = %s", [email])
            user_count = cursor.fetchone()[0]
        if user_count > 0:
            return render(request, 'signup.html', {'error': 'User with this email already exists.'})
        
        # If user doesn't exist, create a new user
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Admin (email, password) VALUES (%s, %s)", [email, password])
        
        return redirect('signin_admin')
    
    return render(request, 'signup.html')


def signin_admin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Check if user with given email and password exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT admin_id FROM Admin WHERE email = %s AND password = %s", [email, password])
            row = cursor.fetchone()
            if row is not None:
                user_id = row[0]
                print(user_id)
                request.session['user_id'] = user_id
                return redirect('home')
            cursor.execute("SELECT student_id FROM Students WHERE email = %s AND password = %s", [email, password])
            col = cursor.fetchone()
            if col is None:
                cursor.execute("SELECT teacher_id FROM Teachers WHERE email = %s AND password = %s", [email, password])
                col = cursor.fetchone()
            if col is not None:
                user_id = col[0]
                print(user_id)
                request.session['user_id'] = user_id
                return redirect('student_home')
            return render(request, 'signin.html', {'error': 'Invalid email or password.'})
    
    return render(request, 'signin.html')

import django

@authenticated
def logout(request):
    django.contrib.auth.logout(request)
    return redirect('home')

def home(request):
    return render(request, 'dashboard.html')

def student_home(request):
    return render(request, 'st_dashboard.html')

@authenticated
def add_student(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM Departments")
        depart= cursor.fetchall()

    context = {item[0]:None for item in depart}

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        department = request.POST['department']
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT department_id FROM Departments WHERE name = %s", [department])
            department_id= cursor.fetchone()
        
        # Insert a new row in the 'students' table
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Students (first_name, last_name, email, phone_number, password, department_id) VALUES (%s, %s, %s, %s, %s, %s)", [first_name, last_name, email, phone_number, password, department_id])
        return redirect('view_students')
    
    
    return render(request, 'add_std.html', {'dep': context})

@authenticated
def view_students(request):
    # Connect to the database
    with connection.cursor() as cursor:
    # Retrieve all rows from the 'students' table
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
    student_details = []
    for student in students:
        # extract each student's details
        student_id, first_name, last_name, email, password, phone_number, department_id = student
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM Departments where department_id=%s", [department_id])
            department = cursor.fetchone()[0]
        student_details.append({'id': student_id, 'first_name': first_name, 'last_name': last_name, 'email': email,
                                'phone_number': phone_number, 'department': department, 'password': password})

    return render(request, 'view_std.html', {'students': student_details})




@authenticated
def edit_student(request, student_id):
    # Connect to the database
    with connection.cursor() as cursor:
        # Retrieve the teacher's details from the 'teachers' table
        cursor.execute("SELECT * FROM Students WHERE student_id = %s", [student_id])
        student = cursor.fetchone()
        
        # If the teacher does not exist, return an error page
        if not student:
            return render(request, 'error.html', {'error': 'Student not found'})
        
        # Extract the teacher's details
        student_id, first_name, last_name, email, phone_number, department_id, password= student
     # Retrieve the name of the teacher's department from the 'departments' table
        
        cursor.execute("SELECT name FROM Departments WHERE department_id = %s", [department_id])
        department_name = cursor.fetchone()
        
        # Retrieve the names of all departments from the 'departments' table
        cursor.execute("SELECT name FROM Departments")
        departments = [department[0] for department in cursor.fetchall()]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM Departments")
        depart= cursor.fetchall()

    context = {item[0]:None for item in depart}

    # If the request is a POST request, update the teacher's details
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        department = request.POST['department']
        print(first_name, last_name)

        with connection.cursor() as cursor:
            cursor.execute("SELECT department_id FROM Departments WHERE name = %s", [department])
            department_id = cursor.fetchone()[0]
        
        # Update the teacher's details in the 'teachers' table
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Students SET first_name = %s, last_name = %s, email = %s, phone_number = %s, password = %s, department_id = %s WHERE student_id = %s", [first_name, last_name, email, phone_number, password, department_id, student_id])
        
        # Redirect the user to the view teachers page
        return redirect('view_students')
    
    # Render the edit teacher page with the teacher's details and the list of departments
    return render(request, 'edit_std.html', {'student_id': student_id, 'first_name': first_name, 'last_name': last_name, 'email': email, 'phone_number': phone_number, 'password': password, 'department_name': department_name, 'departments': departments, 'dep': context})



@authenticated
def delete_student(request, student_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Students WHERE student_id = %s", [student_id])
    return redirect('view_students')




@authenticated
def add_teacher(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM Departments")
        depart= cursor.fetchall()

    context = {item[0]:None for item in depart}

    print(context) 
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        department = request.POST['department']
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT department_id FROM Departments WHERE name = %s", [department])
            department_id= cursor.fetchone()
        
        # Insert a new row in the 'students' table
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Teachers (first_name, last_name, email, phone_number, password, department_id) VALUES (%s, %s, %s, %s, %s, %s)", [first_name, last_name, email, phone_number, password, department_id])
        return redirect('view_teachers')
    
    
    return render(request, 'add_teacher.html', {'dep': context})

@authenticated
def view_teachers(request):
    # Connect to the database
    with connection.cursor() as cursor:
    # Retrieve all rows from the 'students' table
        cursor.execute("SELECT * FROM Teachers")
        teachers = cursor.fetchall()
    teacher_details = []
    for teacher in teachers:
        # extract each student's details
        teacher_id, first_name, last_name, email, password, phone_number, department_id, hire_date = teacher
        print(phone_number)
        with connection.cursor() as cursor:
    # Retrieve all rows from the 'students' table
            cursor.execute("SELECT name FROM Departments where department_id=%s", [department_id])
            department = cursor.fetchone()[0]
        teacher_details.append({'id': teacher_id, 'first_name': first_name, 'last_name': last_name, 'email': email,
                                'phone_number': phone_number, 'department': department, 'password': password, 'hire_date':hire_date})

    return render(request, 'view_teacher.html', {'teachers': teacher_details})


@authenticated
def edit_teacher(request, teacher_id):
    # Connect to the database
    with connection.cursor() as cursor:
        # Retrieve the teacher's details from the 'teachers' table
        cursor.execute("SELECT * FROM Teachers WHERE teacher_id = %s", [teacher_id])
        teacher = cursor.fetchone()
        
        # If the teacher does not exist, return an error page
        if not teacher:
            return render(request, 'error.html', {'error': 'Teacher not found'})
        
        # Extract the teacher's details
        teacher_id, first_name, last_name, email, password, phone_number, department_id, hire_date = teacher
        
        # Retrieve the name of the teacher's department from the 'departments' table
        cursor.execute("SELECT name FROM Departments WHERE department_id = %s", [department_id])
        department_name = cursor.fetchone()[0]
        
        # Retrieve the names of all departments from the 'departments' table
        cursor.execute("SELECT name FROM Departments")
        departments = [department[0] for department in cursor.fetchall()]
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT name FROM Departments")
        depart= cursor.fetchall()

    context = {item[0]:None for item in depart}
    
    # If the request is a POST request, update the teacher's details
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        department = request.POST['department']
        print(first_name, last_name)
        
        # Retrieve the id of the teacher's department from the 'departments' table
        with connection.cursor() as cursor:
            cursor.execute("SELECT department_id FROM Departments WHERE name = %s", [department])
            department_id = cursor.fetchone()[0]
        
        # Update the teacher's details in the 'teachers' table
        with connection.cursor() as cursor:
            cursor.execute("UPDATE Teachers SET first_name = %s, last_name = %s, email = %s, phone_number = %s, password = %s, department_id = %s WHERE teacher_id = %s", [first_name, last_name, email, phone_number, password, department_id, teacher_id])
        
        # Redirect the user to the view teachers page
        return redirect('view_teachers')
    
    # Render the edit teacher page with the teacher's details and the list of departments
    return render(request, 'edit_teacher.html', {'teacher_id': teacher_id, 'first_name': first_name, 'last_name': last_name, 'email': email, 'phone_number': phone_number, 'password': password, 'department_name': department_name, 'departments': departments, 'dep': context})


@authenticated
def delete_teacher(request, teacher_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", [teacher_id])
    return redirect('view_teachers')


@authenticated
def add_department(request):
    if request.method == 'POST':
        name = request.POST['name']

        # Insert a new row in the 'students' table
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO Departments (name) VALUES (%s)", [name])
        return redirect('view_departments')
   
    
    return render(request, 'add_depart.html')


@authenticated
def view_departments(request):
    # Connect to the database
    with connection.cursor() as cursor:
    # Retrieve all rows from the 'students' table
        cursor.execute("SELECT * FROM Departments")
        departments = cursor.fetchall()
    department_details = []
    for department in departments:
        # extract each student's details
        department_id, name= department
        print(department)
        department_details.append({'id': department_id, 'name': name})

    return render(request, 'view_depart.html', {'departments': department_details})

@authenticated
def delete_department(request, department_id):
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Departments WHERE department_id = %s", [department_id])
    return redirect('view_departments')

@authenticated
def v_students(request):
    # Connect to the database
    with connection.cursor() as cursor:
    # Retrieve all rows from the 'students' table
        cursor.execute("SELECT * FROM Students")
        students = cursor.fetchall()
    student_details = []
    for student in students:
        # extract each student's details
        student_id, first_name, last_name, email, password, phone_number, department_id = student
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM Departments where department_id=%s", [department_id])
            department = cursor.fetchone()[0]
        student_details.append({'id': student_id, 'first_name': first_name, 'last_name': last_name, 'email': email,
                                'phone_number': phone_number, 'department': department, 'password': password})

    return render(request, 'v_std.html', {'students': student_details})


@authenticated
def v_departments(request):
    # Connect to the database
    with connection.cursor() as cursor:
    # Retrieve all rows from the 'students' table
        cursor.execute("SELECT * FROM Departments")
        departments = cursor.fetchall()
    department_details = []
    for department in departments:
        # extract each student's details
        department_id, name= department
        print(department)
        department_details.append({'id': department_id, 'name': name})

    return render(request, 'v_depart.html', {'departments': department_details})


@authenticated
def v_teachers(request):
    # Connect to the database
    with connection.cursor() as cursor:
    # Retrieve all rows from the 'students' table
        cursor.execute("SELECT * FROM Teachers")
        teachers = cursor.fetchall()
    teacher_details = []
    for teacher in teachers:
        # extract each student's details
        teacher_id, first_name, last_name, email, password, phone_number, department_id, hire_date = teacher
        print(phone_number)
        with connection.cursor() as cursor:
    # Retrieve all rows from the 'students' table
            cursor.execute("SELECT name FROM Departments where department_id=%s", [department_id])
            department = cursor.fetchone()[0]
        teacher_details.append({'id': teacher_id, 'first_name': first_name, 'last_name': last_name, 'email': email,
                                'phone_number': phone_number, 'department': department, 'password': password, 'hire_date':hire_date})

    return render(request, 'v_teacher.html', {'teachers': teacher_details})