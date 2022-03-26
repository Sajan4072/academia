from django.shortcuts import render, redirect
from admins.models import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from authentications.auth import lecturer_only
from authentications.models import *
from .filters import *
from .forms import *
from .models import *
from admins.filters import *
from admins.forms import *
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash



@login_required
@lecturer_only
def lecturer_dashboard(request):
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
    return render(request, 'lecturers/dashboard.html', context)


@login_required
@lecturer_only
def show_students(request):
    students = User.objects.filter(is_staff=0,is_superuser=0).order_by('-id')
    student_filter = UserFilter(request.GET, queryset=students)
    student_final = student_filter.qs
    context = {
        'students':student_final,
        'student_filter':student_filter
    }
    return render(request, 'lecturers/show_students.html', context)


@login_required
@lecturer_only
def profile_students(request, username):
    instance = Profile.objects.get(username=username)
    context ={
        'student': instance
    }
    return render(request, 'lecturers/profile_students.html', context)


@login_required
@lecturer_only
def profile_others(request):
    instance = Others.objects.get(username=request.user.username)
    if request.method=='POST':
        userdata = ProfileFormOthers2(request.POST, request.FILES, instance=instance)
        if userdata.is_valid():
            userdata.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully.' )
            #return redirect('/admins/show_admins')
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'lecturers/profile_others.html',context)

    context ={
        'form' : ProfileFormOthers2(instance=instance),
        'student': instance
    }
    return render(request, 'lecturers/profile_others.html', context)


@login_required
@lecturer_only
def show_modules(request):
    results = UserModule.objects.filter(user=request.user).order_by('-id')
    context = {
        'results':results,
    }
    return render(request, 'lecturers/show_modules.html',context)



@login_required
@lecturer_only
def password_change_lecturer(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Password Changed Successfully')
            return redirect('/lecturers')

        else:
            messages.add_message(request, messages.ERROR, 'Please verify the form fields')
            return render(request, 'lecturers/password_change.html', {'form':form})
    context = {
        'form':PasswordChangeForm(request.user)
    }
    return render(request, 'lecturers/password_change.html', context)


@login_required
@lecturer_only
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
    week2a = Assignment.objects.filter(week="WEEK2", module=module.id)
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
    return render(request, 'lecturers/show_module_details.html',context)


@login_required
@lecturer_only
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
            return redirect('/lecturers/show_module_details/'+str(module.id))
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'lecturers/add_contents.html',context)
    context ={'form' : ModuleContentForm(instance=module)}
    return render(request, 'lecturers/add_contents.html', context)

@login_required
@lecturer_only
def delete_contents(request, id):
    content = ModuleContent.objects.get(id=id)
    module = content.module
    content.delete()
    messages.add_message(request, messages.SUCCESS, 'Content deleted successfully')
    return redirect('/lecturers/show_module_details/'+str(module.id))


@login_required
@lecturer_only
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
            return redirect('/lecturers/show_module_details/'+str(module.id))
        else:
            context = {'form' : userdata}
            messages.add_message(request, messages.ERROR, 'Bad Credentials!' )
            return render(request, 'lecturers/add_assignments.html',context)
    context ={'form' : AssignmentForm(instance=module)}
    return render(request, 'lecturers/add_assignments.html', context)

@login_required
@lecturer_only
def delete_assignments(request, id):
    content = Assignment.objects.get(id=id)
    module = content.module
    content.delete()
    messages.add_message(request, messages.SUCCESS, 'Assignment deleted successfully')
    return redirect('/lecturers/show_module_details/'+str(module.id))


@login_required
@lecturer_only
def show_submissions(request, assignmentid):
    assignment = Assignment.objects.get(id=assignmentid)
    submissions = SubmitAssignment.objects.filter(assignment=assignment).order_by('-id')
    student_filter = AssignmentSubmissionFilter2(request.GET, queryset=submissions)
    student_final = student_filter.qs
    context = {
        'results':student_final,
        'student_filter': student_filter
    }
    return render(request, 'lecturers/show_submissions.html', context)