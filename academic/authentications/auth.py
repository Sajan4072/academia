from django.shortcuts import redirect


def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/students')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function


def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff and request.user.is_superuser:
            return view_function(request, *args, **kwargs)
        elif request.user.is_staff and not request.user.is_superuser:
            return redirect('/lecturers')
        elif not request.user.is_staff and not request.user.is_superuser:
            return redirect('/students')
    return wrapper_function


def student_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if not request.user.is_staff and not request.user.is_superuser:
            return view_function(request, *args, **kwargs)
        elif request.user.is_staff and  request.user.is_superuser:
            return redirect('/admins')
        elif request.user.is_staff and not request.user.is_superuser:
            return redirect('/lecturers')
    return wrapper_function


def lecturer_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff and not request.user.is_superuser:
            return view_function(request, *args, **kwargs)
        elif request.user.is_staff and  request.user.is_superuser:
            return redirect('/admins')
        elif  not request.user.is_staff and not request.user.is_superuser:
            return redirect('/students')
    return wrapper_function