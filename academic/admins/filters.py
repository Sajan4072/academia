import django_filters
from django.contrib.auth.models import User
from django_filters import CharFilter
from .models import Result, UserModule, Modules, SubmitAssignment, Fees


class UserFilter(django_filters.FilterSet):
    username = CharFilter(field_name='username', lookup_expr='icontains')
    email = CharFilter(field_name='email', lookup_expr='icontains')
    class Meta:
        model = User
        fields = ''

class ResultFilter(django_filters.FilterSet):
    username = CharFilter(field_name='studentid', lookup_expr='icontains')
    fullname = CharFilter(field_name='fullname', lookup_expr='icontains')
    class Meta:
        model = Result
        fields = ''

class ModuleFilter(django_filters.FilterSet):
    module_code = CharFilter(field_name='module_code', lookup_expr='icontains')
    module_name= CharFilter(field_name='module_name', lookup_expr='icontains')
    class Meta:
        model = Modules
        fields = ''

class ModuleAccessFilter(django_filters.FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='icontains')
    class Meta:
        model = UserModule
        fields = ''


class AssignmentSubmissionFilter(django_filters.FilterSet):
    modulecode = CharFilter(field_name='module__module_code', lookup_expr='icontains')
    modulename = CharFilter(field_name='module__module_name', lookup_expr='icontains')
    assignmentname = CharFilter(field_name='assignment__title', lookup_expr='icontains')
    class Meta:
        model = SubmitAssignment
        fields = ''


class AssignmentSubmissionFilter2(django_filters.FilterSet):
    username = CharFilter(field_name='user__username', lookup_expr='icontains')
    class Meta:
        model = SubmitAssignment
        fields = ''


class FeeFilter(django_filters.FilterSet):
    class Meta:
        model = Fees
        fields = ['batch','semester']
