from django import forms
from myapp.models import User

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_pic','email','first_name','last_name','username']


GENDER_CHOICES = [
    ('Male','Male'),
    ('Female','Female'),
]

class AddStaffForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect())
    address = forms.CharField(max_length=255)
    password = forms.CharField(max_length=100)
    
    class Meta:
        model = User
        fields = ['profile_pic','email','first_name','last_name','username']

class UpdateStaffForm(AddStaffForm):
    password = forms.CharField(max_length=100,required=False)
    
    
        

