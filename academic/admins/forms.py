from django.forms import ModelForm
from authentications.models import Profile, Others
from .models import *


class ProfileFormStudent(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude =['email', 'username','user']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']


class ProfileFormOthers(ModelForm):
    class Meta:
        model = Others
        fields = '__all__'
        exclude =['email', 'username','user']


class ProfileFormOthers2(ModelForm):
    class Meta:
        model = Others
        fields = ['profile_pic']


class ResultFileForm(ModelForm):
    class Meta:
        model = ResultFile
        fields = '__all__'


class ResultForm(ModelForm):
    class Meta:
        model = Result
        fields = '__all__'


class CourseForm(ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'


class ModuleForm(ModelForm):
    class Meta:
        model = Modules
        fields = '__all__'


class ModuleContentForm(ModelForm):
    class Meta:
        model = ModuleContent
        fields = ['week','title','content']


class AssignmentForm(ModelForm):
    class Meta:
        model = Assignment
        fields = ['week','title','assignment_file', 'deadline']


class FeesForm(ModelForm):
    class Meta:
        model = Fees
        fields = '__all__'


class EnquiriesForm(ModelForm):
    class Meta:
        model = Enquiries
        fields = '__all__'

class ModuleAccessForm(ModelForm):
    class Meta:
        model = UserModule
        fields = ['user']


class SubmitAssignmentForm(ModelForm):
    class Meta:
        model = SubmitAssignment
        fields = ['title', 'submission_file']