from django import forms
from myapp.models import StaffLeave


class ApplyLeaveForm(forms.ModelForm):
    class Meta:
        model = StaffLeave
        fields = ['leave_type','from_date','to_date','message']
        