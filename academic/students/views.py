from django.shortcuts import render, redirect
from admins.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentications.auth import student_only
from authentications.models import *
from .filters import *
from .forms import *
from .models import *
from admins.filters import *
from admins.forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

import io, csv, pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression, LinearRegression

@login_required
@student_only
def student_dashboard(request):
    results = UserModule.objects.filter(user=request.user).order_by('-id')
    context = {
        'results': results,
    }
    return render(request, 'students/dashboard.html', context)


@login_required
@student_only
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
    return render(request, 'students/show_module_details.html',context)


@login_required
@student_only
def show_detail_results(request):
    results = Result.objects.filter(studentid=request.user.username)
    if results:
        stu_name = Result.objects.values_list('fullname', flat=True).filter(studentid=request.user.username, semester=1)
        marks1 = Result.objects.values_list('marks', flat=True).filter(studentid=request.user.username, semester=1)
        marks2 = Result.objects.values_list('marks', flat=True).filter(studentid=request.user.username, semester=2)
        marks3 = Result.objects.values_list('marks', flat=True).filter(studentid=request.user.username, semester=3)
        marks4 = Result.objects.values_list('marks', flat=True).filter(studentid=request.user.username, semester=4)
        marks5 = Result.objects.values_list('marks', flat=True).filter(studentid=request.user.username, semester=5)
        marks6 = Result.objects.values_list('marks', flat=True).filter(studentid=request.user.username, semester=6)
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
        return render(request, 'students/show_results_details.html',context)
    else:
        context = {
            'message': 'Sorry, no results found'
        }
        return render(request, 'students/show_results_details.html', context)


@login_required
@student_only
def profile_students_students(request):
    instance = Profile.objects.get(username=request.user.username)
    if request.method=='POST':
        userdata = ProfileForm(request.POST, request.FILES, instance=instance)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully.' )
            #return redirect('/admins/show_admins')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'students/profile_students.html',context)

    context ={
        'form' : ProfileForm(instance=instance),
        'student': instance
    }
    return render(request, 'students/profile_students.html', context)

@login_required
@student_only
def password_change_student(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Password Changed Successfully')
            return redirect('/students')

        else:
            messages.add_message(request, messages.ERROR, 'Please verify the form fields')
            return render(request, 'students/password_change.html', {'form':form})
    context = {
        'form':PasswordChangeForm(request.user)
    }
    return render(request, 'students/password_change.html', context)


@login_required
@student_only
def submit_assignments(request, moduleid, assignmentid):
    user = request.user
    assignment = Assignment.objects.get(id=assignmentid)
    module = Modules.objects.get(id=moduleid)
    if request.method=='POST':
        previous_submission = SubmitAssignment.objects.filter(user=user.id, assignment=assignment.id, module=module.id)
        if previous_submission:
            messages.add_message(request, messages.ERROR, 'Assignment already submitted. You cannot submit twice.')
            return redirect('/students/show_module_details/'+str(module.id))
        else:
            userdata = SubmitAssignmentForm(request.POST, request.FILES)
            if userdata.is_valid():
                SubmitAssignment.objects.create(user=user,
                                                module=module,
                                                assignment=assignment,
                                                title = request.POST['title'],
                                                submission_file=request.FILES['submission_file'])
                messages.add_message(request, messages.SUCCESS, 'Assignment Submitted Successfully.' )
                return redirect('/students/show_submissions')
            else:
                context = {'form' : userdata}
                messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
                return render(request, 'students/submit_assignments.html',context)

    context ={
        'form' : SubmitAssignmentForm,
    }
    return render(request, 'students/submit_assignments.html', context)


@login_required
@student_only
def show_submissions(request):
    submissions = SubmitAssignment.objects.filter(user=request.user).order_by('-id')
    student_filter = AssignmentSubmissionFilter(request.GET, queryset=submissions)
    student_final = student_filter.qs
    context = {
        'results':student_final,
        'student_filter': student_filter
    }
    return render(request, 'students/show_submissions.html', context)


@login_required
@student_only
def delete_submissions(request, submissionid):
    submission = SubmitAssignment.objects.get(id=submissionid)
    submission.delete()
    messages.add_message(request, messages.SUCCESS, 'Selected Submission Deleted Successfully')
    return redirect('/students/show_submissions')


@login_required
@student_only
def show_fees(request):
    results = Fees.objects.filter(batch=request.user.profile.batch, course=request.user.profile.course.id).order_by('-id')
    context = {
        'results': results
    }
    return render(request, 'students/show_fees.html',context)