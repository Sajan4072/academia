from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_modules, name="lecturer_dashboard"),
    path('show_students', views.show_students, name='show_students_lecturer'),
    path('profile_students/<str:username>', views.profile_students, name='profile_students_lecturer'),
    path('profile_others', views.profile_others, name='profile_others_lecturer'),
    path('show_modules', views.show_modules, name='show_modules_lecturer'),
    path('password_change_lecturer', views.password_change_lecturer, name='password_change_lecturer'),
    path('show_module_details/<str:moduleid>', views.show_module_details, name='show_module_details_lecturer'),
    path('add_contents/<str:moduleid>', views.add_contents, name='add_contents_lecturer'),
    path('delete_contents/<str:id>', views.delete_contents, name='delete_contents_lecturer'),
    path('add_assignments/<str:moduleid>', views.add_assignments, name='add_assignments_lecturer'),
    path('delete_assignments/<str:id>', views.delete_assignments, name='delete_assignments_lecturer'),
    path('show_submissions/<str:assignmentid>', views.show_submissions, name='show_submissions_lecturer'),
]