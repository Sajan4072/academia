from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentications.auth import admin_only
from authentications.forms import CreateUserForm
from authentications.models import Profile, Others
from .filters import *
from .forms import *
from .models import *

import io, csv, pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression

@login_required
@admin_only
def admin_dashboard(request):
    students = User.objects.filter(is_staff=0, is_superuser=0)
    student_count = students.count()
    lecturers = User.objects.filter(is_staff=1, is_superuser=0)
    lecturer_count = lecturers.count()
    admins = User.objects.filter(is_staff=1, is_superuser=1)
    admin_count = admins.count()
    results = Result.objects.all()
    result_count = results.count()
    courses = Courses.objects.all()
    course_count = courses.count()
    modules = Modules.objects.all()
    module_count = modules.count()
    fees = Fees.objects.all()
    fee_count = fees.count()
    assignments = Assignment.objects.all()
    assignment_count = assignments.count()
    enquiries = Enquiries.objects.all()
    enquiry_count = enquiries.count()

    context = {
        'student': student_count,
        'lecturer': lecturer_count,
        'result': result_count,
        'course': course_count,
        'module':module_count,
        'admin': admin_count,
        'fee':fee_count,
        'assignment':assignment_count,
        'enquiry':enquiry_count
    }
    return render(request, 'admins/dashboard.html', context)


@login_required
@admin_only
def signup_students(request):
    if request.method=='POST':
        userdata = CreateUserForm(request.POST)
        if userdata.is_valid():
            user = userdata.save()
            Profile.objects.create(user=user, username=user.username, email= user.email)
            messages.add_message(request, messages.SUCCESS, 'Student registered successfully!' )
            return redirect('/admins/show_students')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/signup_students.html',context)
    context ={'form' : CreateUserForm}
    return render(request, 'admins/signup_students.html', context)


@login_required
@admin_only
def signup_lecturers(request):
    if request.method=='POST':
        userdata = CreateUserForm(request.POST)
        if userdata.is_valid():
            user = userdata.save()
            Others.objects.create(user=user, username=user.username, email= user.email)
            user.is_staff = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Lecturer Registered Successfully' )
            return redirect('/admins/show_lecturers')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/signup_lecturers.htm',context)

    context ={'form' : CreateUserForm}
    return render(request, 'admins/signup_lecturers.htm', context)


@login_required
@admin_only
def signup_admins(request):
    if request.method=='POST':
        userdata = CreateUserForm(request.POST)
        if userdata.is_valid():
            user = userdata.save()
            Others.objects.create(user=user, username=user.username, email= user.email)
            user.is_staff = True
            user.is_superuser = True
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Admin Registered Successfully.' )
            return redirect('/admins/show_admins')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/signup_admins.html',context)

    context ={'form' : CreateUserForm}
    return render(request, 'admins/signup_admins.html', context)


@login_required
@admin_only
def show_students(request):
    students = User.objects.filter(is_staff=0,is_superuser=0).order_by('-id')
    student_filter = UserFilter(request.GET, queryset=students)
    student_final = student_filter.qs
    context = {
        'students':student_final,
        'student_filter':student_filter
    }
    return render(request, 'admins/show_students.html', context)


@login_required
@admin_only
def show_lecturers(request):
    lecturers = User.objects.filter(is_staff=1,is_superuser=0).order_by('-id')
    student_filter = UserFilter(request.GET, queryset=lecturers)
    student_final = student_filter.qs
    context = {
        'lecturers':student_final,
        'student_filter': student_filter
    }
    return render(request, 'admins/show_lecturers.html', context)


@login_required
@admin_only
def show_admins(request):
    #admins = User.objects.filter(is_staff=1,is_superuser=1).order_by('-id').exclude(id=request.user.id)
    admins = User.objects.filter(is_staff=1, is_superuser=1).order_by('-id')
    student_filter = UserFilter(request.GET, queryset=admins)
    student_final = student_filter.qs
    context = {
        'admins':student_final,
        'student_filter': student_filter
    }
    return render(request, 'admins/show_admins.html', context)


@login_required
@admin_only
def delete_students(request, username):
    student = User.objects.get(username=username)
    student.delete()
    messages.add_message(request, messages.SUCCESS, 'Selected Student Deleted Successfully')
    return redirect('/admins/show_students')


@login_required
@admin_only
def delete_lecturers(request, username):
    student = User.objects.get(username=username)
    student.delete()
    messages.add_message(request, messages.SUCCESS, 'Selected Lecturer Deleted Successfully')
    return redirect('/admins/show_lecturers')


@login_required
@admin_only
def delete_admins(request, username):
    student = User.objects.get(username=username)
    student.delete()
    messages.add_message(request, messages.SUCCESS, 'Selected Admin Deleted Successfully')
    return redirect('/admins/show_admins')

@login_required
@admin_only
def profile_students(request, username):
    instance = Profile.objects.get(username=username)
    if request.method=='POST':
        userdata = ProfileFormStudent(request.POST, request.FILES, instance=instance)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully.' )
            #return redirect('/admins/show_admins')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/profile_students.html',context)

    context ={
        'form' : ProfileFormStudent(instance=instance),
        'student': instance
    }
    return render(request, 'admins/profile_students.html', context)


@login_required
@admin_only
def profile_others(request, username):
    instance = Others.objects.get(username=username)
    if request.method=='POST':
        userdata = ProfileFormOthers(request.POST, request.FILES, instance=instance)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully.' )
            #return redirect('/admins/show_admins')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/profile_others.html',context)

    context ={
        'form' : ProfileFormOthers(instance=instance),
        'student': instance
    }
    return render(request, 'admins/profile_others.html', context)


@login_required
@admin_only
def add_results(request):
    if request.method == 'POST':
        file = request.FILES['file']
        reader = pd.read_csv(file, on_bad_lines='skip')
        reader.fillna(0, inplace=True)
        for _, row in reader.iterrows():
            new_file = Result(
                studentid=row["Student ID"],
                fullname=row['Fullname'],
                subject=row["Subject"],
                course=row["Course"],
                semester=row["Semester"],
                coursework=row["Cw"],
                exam=row["Ex"],
                marks=row["Mm"],
                status=row["Status"],
            )
            new_file.save()
        resultfile = ResultFileForm(request.POST, request.FILES)
        if resultfile.is_valid():
            resultfile.save()
        messages.add_message(request, messages.SUCCESS, 'Result Added Successfully.')
        return redirect('/admins/show_results')
    context = {
        'form':ResultFileForm
    }
    return render(request, 'admins/add_results.html', context)


@login_required
@admin_only
def show_results(request):
    results = Result.objects.all().values('studentid','fullname').distinct()
    student_filter = ResultFilter(request.GET, queryset=results)
    student_final = student_filter.qs
    context = {
        'results':student_final,
        'student_filter':student_filter
    }
    return render(request, 'admins/show_results.html',context)


@login_required
@admin_only
def show_results_all(request):
    results = Result.objects.all().order_by('-id')
    student_filter = ResultFilter(request.GET, queryset=results)
    student_final = student_filter.qs
    context = {
        'results':student_final,
        'student_filter':student_filter
    }
    return render(request, 'admins/show_results_all.html',context)


@login_required
@admin_only
def show_detail_results(request,studentid):
    results = Result.objects.filter(studentid=studentid)
    stu_name = Result.objects.values_list('fullname', flat=True).filter(studentid=studentid, semester=1)
    marks1 = Result.objects.values_list('marks', flat=True).filter(studentid=studentid, semester=1)
    marks2 = Result.objects.values_list('marks', flat=True).filter(studentid=studentid, semester=2)
    marks3 = Result.objects.values_list('marks', flat=True).filter(studentid=studentid, semester=3)
    marks4 = Result.objects.values_list('marks', flat=True).filter(studentid=studentid, semester=4)
    marks5 = Result.objects.values_list('marks', flat=True).filter(studentid=studentid, semester=5)
    marks6 = Result.objects.values_list('marks', flat=True).filter(studentid=studentid, semester=6)
    result_data = pd.read_csv('static/data/TestData.csv')
    X = result_data.drop(['pct','id'],axis=1)
    Y = result_data['pct']
    X_train,X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.3, random_state=2)
    model =LinearRegression()
    model.fit(X_train,Y_train)
    if marks1:
        input_data2=(marks1[0],marks1[1],marks1[2],marks1[3])
        input_data_as_numpy_array2 = np.asarray(input_data2)
        input_date_reshaped2 = input_data_as_numpy_array2.reshape(1,-1)
        prediction2 = round(model.predict(input_date_reshaped2)[0],2)
        actual1 = (marks1[0] + marks1[1] + marks1[2] + marks1[3]) / 4
    if not marks1:
        prediction2='We cannot predict the performance as there is no previous result of first semester'
        actual1 = 'Sorry, we cannot find results.'

    if marks2:
        input_data3 = (marks2[0], marks2[1], marks2[2], marks2[3])
        input_data_as_numpy_array3 = np.asarray(input_data3)
        input_date_reshaped3 = input_data_as_numpy_array3.reshape(1, -1)
        prediction3 = round(model.predict(input_date_reshaped3)[0],2)
        actual2= (marks2[0]+marks2[1]+marks2[2]+marks2[3])/4
    if not marks2:
        prediction3='We cannot predict the performance as there is no previous result of second semester.'
        actual2='Sorry, we cannot find results.'

    if marks3:
        input_data4 = (marks3[0], marks3[1], marks3[2], marks3[3])
        input_data_as_numpy_array4 = np.asarray(input_data4)
        input_date_reshaped4 = input_data_as_numpy_array4.reshape(1, -1)
        prediction4 = round(model.predict(input_date_reshaped4)[0],2)
        actual3 = (marks3[0] + marks3[1] + marks3[2] + marks3[3]) / 4
    if not marks3:
        prediction4='We cannot predict the performance as there is no previous result of third semester.'
        actual3 = 'Sorry, we cannot find results.'

    if marks4:
        input_data5 = (marks4[0], marks4[1], marks4[2], marks4[3])
        input_data_as_numpy_array5 = np.asarray(input_data5)
        input_date_reshaped5 = input_data_as_numpy_array5.reshape(1, -1)
        prediction5 = round(model.predict(input_date_reshaped5)[0],2)
        actual4 = (marks4[0] + marks4[1] + marks4[2] + marks4[3]) / 4
    if not marks4:
        prediction5='We cannot predict the performance as there is no previous result of fourth semester.'
        actual4 = 'Sorry, we cannot find results.'

    if marks5:
        input_data6 = (marks5[0], marks5[1], marks5[2], marks5[3])
        input_data_as_numpy_array6 = np.asarray(input_data6)
        input_date_reshaped6 = input_data_as_numpy_array6.reshape(1, -1)
        prediction6 = round(model.predict(input_date_reshaped6)[0],2)
        actual5 = (marks5[0] + marks5[1] + marks5[2] + marks5[3]) / 4
    if not marks5:
        prediction6='We cannot predict the performance as there is no previous result of fifth semester.'
        actual5 = 'Sorry, we cannot find results.'

    if marks6:
        actual6 = (marks6[0] + marks6[1] + marks6[2] + marks6[3]) / 4
    if not marks6:
        actual6 = 'Sorry, we cannot find results.'
    print('Actual6th', actual6)

    context = {'results': results,
               'stu_name': stu_name[0],
               'actual1': actual1,
               'prediction2':prediction2,
               'actual2': actual2,
               'prediction3': prediction3,
               'actual3': actual3,
               'prediction4': prediction4,
               'actual4': actual4,
               'prediction5': prediction5,
               'actual5': actual5,
               'prediction6': prediction6,
               'actual6':actual6
               }
    return render(request, 'admins/show_result_details.html',context)


@login_required
@admin_only
def add_results_manual(request):
    if request.method=='POST':
        userdata = ResultForm(request.POST)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Result Added Successfully.' )
            return redirect('/admins/show_results')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/add_results_manual.html',context)

    context ={'form' : ResultForm}
    return render(request, 'admins/add_results_manual.html', context)


@login_required
@admin_only
def delete_results(request, studentid):
    student = Result.objects.filter(studentid=studentid)
    student.delete()
    messages.add_message(request, messages.SUCCESS, 'Result Deleted Successfully')
    return redirect('/admins/show_results')


@login_required
@admin_only
def delete_results_by_id(request, id):
    student = Result.objects.get(id=id)
    student.delete()
    messages.add_message(request, messages.SUCCESS, 'Result Deleted Successfully')
    return redirect('/admins/show_results_all')


@login_required
@admin_only
def add_courses(request):
    if request.method=='POST':
        userdata = CourseForm(request.POST, request.FILES)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Course added successfully!' )
            return redirect('/admins/show_courses')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/add_courses.html',context)
    context ={'form' : CourseForm}
    return render(request, 'admins/add_courses.html', context)


@login_required
@admin_only
def show_courses(request):
    results = Courses.objects.all().order_by('-id')
    context = {
        'results':results,
    }
    return render(request, 'admins/show_courses.html',context)


@login_required
@admin_only
def update_courses(request, courseid):
    course = Courses.objects.get(id=courseid)
    if request.method=='POST':
        userdata = CourseForm(request.POST, request.FILES, instance=course)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Course updated successfully!' )
            return redirect('/admins/show_courses')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/update_courses.html',context)
    context ={'form' : CourseForm(instance=course)}
    return render(request, 'admins/update_courses.html', context)


@login_required
@admin_only
def delete_courses(request, courseid):
    course = Courses.objects.get(id=courseid)
    course.delete()
    messages.add_message(request, messages.SUCCESS, 'Course deleted successfully')
    return redirect('/admins/show_courses')


@login_required
@admin_only
def add_modules(request):
    if request.method=='POST':
        userdata = ModuleForm(request.POST, request.FILES)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Module added successfully!' )
            return redirect('/admins/show_modules')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/add_modules.html',context)
    context ={'form' : ModuleForm}
    return render(request, 'admins/add_modules.html', context)


@login_required
@admin_only
def show_modules(request):
    results = Modules.objects.all().order_by('-id')
    student_filter = ModuleFilter(request.GET, queryset=results)
    student_final = student_filter.qs
    context = {
        'results':student_final,
        'student_filter':student_filter
    }
    return render(request, 'admins/show_modules.html',context)


@login_required
@admin_only
def show_module_details(request, moduleid):
    module = Modules.objects.get(id=moduleid)
    assignments = Assignment.objects.filter(module=module.id)
    week1 = ModuleContent.objects.filter(week="WEEK1",module=module.id)
    week2 = ModuleContent.objects.filter(week="WEEK2", module=module.id)
    week3 = ModuleContent.objects.filter(week="WEEK3", module=module.id)
    week4 = ModuleContent.objects.filter(week="WEEK4", module=module.id)
    week5 = ModuleContent.objects.filter(week="WEEK5", module=module.id)
    week6 = ModuleContent.objects.filter(week="WEEK6", module=module.id)
    week7 = ModuleContent.objects.filter(week="WEEK7", module=module.id)
    week8 = ModuleContent.objects.filter(week="WEEK8", module=module.id)
    week9 = ModuleContent.objects.filter(week="WEEK9", module=module.id)
    week10 = ModuleContent.objects.filter(week="WEEK10", module=module.id)
    week11 = ModuleContent.objects.filter(week="WEEK11", module=module.id)
    week1a = Assignment.objects.filter(week="WEEK1", module=module.id)
    week2a = Assignment.objects.filter(week="WEEK2", module=module.id)
    week3a = Assignment.objects.filter(week="WEEK3", module=module.id)
    week4a = Assignment.objects.filter(week="WEEK4", module=module.id)
    week5a = Assignment.objects.filter(week="WEEK5", module=module.id)
    week6a = Assignment.objects.filter(week="WEEK6", module=module.id)
    week7a = Assignment.objects.filter(week="WEEK7", module=module.id)
    week8a = Assignment.objects.filter(week="WEEK8", module=module.id)
    week9a = Assignment.objects.filter(week="WEEK9", module=module.id)
    week10a = Assignment.objects.filter(week="WEEK10", module=module.id)
    week11a = Assignment.objects.filter(week="WEEK11", module=module.id)
    context = {
        'module': module,
        'week1': week1,
        'week2': week2,
        'week3': week3,
        'week4': week4,
        'week5': week5,
        'week6': week6,
        'week7': week7,
        'week8': week8,
        'week9': week9,
        'week10': week10,
        'week11': week11,
        'week1a': week1a,
        'week2a': week2a,
        'week3a': week3a,
        'week4a': week4a,
        'week5a': week5a,
        'week6a': week6a,
        'week7a': week7a,
        'week8a': week8a,
        'week9a': week9a,
        'week10a': week10a,
        'week11a': week11a,
        'assignments':assignments
    }
    return render(request, 'admins/show_module_details.html',context)


@login_required
@admin_only
def update_modules(request, moduleid):
    module = Modules.objects.get(id=moduleid)
    if request.method=='POST':
        userdata = ModuleForm(request.POST, request.FILES, instance=module)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Module updated successfully!' )
            return redirect('/admins/show_modules')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/update_modules.html',context)
    context ={'form' : ModuleForm(instance=module)}
    return render(request, 'admins/update_modules.html', context)


@login_required
@admin_only
def delete_modules(request, moduleid):
    module = Modules.objects.get(id=moduleid)
    module.delete()
    messages.add_message(request, messages.SUCCESS, 'Module deleted successfully')
    return redirect('/admins/show_modules')

@login_required
@admin_only
def add_contents(request, moduleid):
    module = Modules.objects.get(id=moduleid)
    course = Courses.objects.get(id=module.course.id)
    if request.method=='POST':
        userdata = ModuleContentForm(request.POST, request.FILES)
        if userdata.is_valid():
            ModuleContent.objects.create(course=course,
                                         module=module,
                                         title=request.POST['title'],
                                         week=request.POST['week'],
                                         content=request.FILES['content'])
            messages.add_message(request, messages.SUCCESS, 'Content added successfully!' )
            return redirect('/admins/show_module_details/'+str(module.id))
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/add_contents.html',context)
    context ={'form' : ModuleContentForm(instance=module)}
    return render(request, 'admins/add_contents.html', context)

@login_required
@admin_only
def delete_contents(request, id):
    content = ModuleContent.objects.get(id=id)
    module = content.module
    content.delete()
    messages.add_message(request, messages.SUCCESS, 'Content deleted successfully')
    return redirect('/admins/show_module_details/'+str(module.id))


@login_required
@admin_only
def add_assignments(request, moduleid):
    module = Modules.objects.get(id=moduleid)
    course = Courses.objects.get(id=module.course.id)
    if request.method=='POST':
        userdata = AssignmentForm(request.POST, request.FILES)
        if userdata.is_valid():
            Assignment.objects.create(course=course,
                                         module=module,
                                         title=request.POST['title'],
                                         week=request.POST['week'],
                                         deadline=request.POST['deadline'],
                                         assignment_file=request.FILES['assignment_file'])
            messages.add_message(request, messages.SUCCESS, 'Assignment added successfully!' )
            return redirect('/admins/show_module_details/'+str(module.id))
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/add_assignments.html',context)
    context ={'form' : AssignmentForm(instance=module)}
    return render(request, 'admins/add_assignments.html', context)

@login_required
@admin_only
def delete_assignments(request, id):
    content = Assignment.objects.get(id=id)
    module = content.module
    content.delete()
    messages.add_message(request, messages.SUCCESS, 'Assignment deleted successfully')
    return redirect('/admins/show_module_details/'+str(module.id))


@login_required
@admin_only
def add_fees(request):
    if request.method=='POST':
        userdata = FeesForm(request.POST, request.FILES)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Fee added successfully!' )
            return redirect('/admins/show_fees')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/add_fees.html',context)
    context ={'form' : FeesForm}
    return render(request, 'admins/add_fees.html', context)


@login_required
@admin_only
def show_fees(request):
    results = Fees.objects.all().order_by('-id')
    student_filter = FeeFilter(request.GET, queryset=results)
    student_final = student_filter.qs
    context = {
        'results': student_final,
        'student_filter': student_filter
    }
    return render(request, 'admins/show_fees.html',context)


@login_required
@admin_only
def update_fees(request, feeid):
    fee = Fees.objects.get(id=feeid)
    if request.method=='POST':
        userdata = FeesForm(request.POST, request.FILES, instance=fee)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Fee updated successfully!' )
            return redirect('/admins/show_fees')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/update_fees.html',context)
    context ={'form' : FeesForm(instance=fee)}
    return render(request, 'admins/update_fees.html', context)


@login_required
@admin_only
def delete_fees(request, feeid):
    fee = Fees.objects.get(id=feeid)
    fee.delete()
    messages.add_message(request, messages.SUCCESS, 'Fee deleted successfully')
    return redirect('/admins/show_fees')


@login_required
@admin_only
def show_module_access(request, moduleid):
    module = Modules.objects.get(id=moduleid)
    module_final = UserModule.objects.filter(module=module).order_by('-id')
    student_filter = ModuleAccessFilter(request.GET, queryset=module_final)
    student_final = student_filter.qs
    context = {
        'results':student_final,
        'module':module,
        'student_filter':student_filter
    }
    return render(request, 'admins/show_module_access.html', context)


@login_required
@admin_only
def add_module_access(request,moduleid):
    module = Modules.objects.get(id=moduleid)
    if request.method=='POST':
        userdata = ModuleAccessForm(request.POST)
        if userdata.is_valid():
            user=userdata.save()
            user.module = module
            user.save()
            messages.add_message(request, messages.SUCCESS, 'Access added successfully!' )
            return redirect('/admins/show_module_access/'+str(module.id))
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'admins/add_module_access.html',context)
    context ={'form' : ModuleAccessForm}
    return render(request, 'admins/add_module_access.html', context)


@login_required
@admin_only
def delete_module_access(request, moduleid, userid):
    module = Modules.objects.get(id=moduleid)
    user = User.objects.get(id=userid)
    access = UserModule.objects.filter(user=user.id,module=module.id)
    access.delete()
    messages.add_message(request, messages.SUCCESS, 'Module access deleted successfully')
    return redirect('/admins/show_module_access/'+str(module.id))


@login_required
@admin_only
def show_enquiries(request):
    results = Enquiries.objects.all().order_by('-id')
    context = {
        'results':results,
    }
    return render(request, 'admins/show_enquiries.html',context)