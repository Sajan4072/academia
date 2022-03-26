from django.urls import path
from . import views

urlpatterns = [
    path('', views.student_dashboard, name="student_dashboard"),
    path('show_module_details/<str:moduleid>', views.show_module_details, name='show_module_details_student'),
    path('submit_assignments/<str:moduleid>/<str:assignmentid>', views.submit_assignments, name='submit_assignments'),
    path('show_submissions', views.show_submissions, name='show_submissions'),
    path('delete_submissions/<str:submissionid>', views.delete_submissions, name='delete_submissions'),
    path('show_detail_results', views.show_detail_results, name='show_detail_results_student'),
    path('profile_students_students', views.profile_students_students, name='profile_students_students'),
    path('password_change_student', views.password_change_student, name='password_change_student'),
    path('show_fees', views.show_fees, name="show_fees_students"),
]