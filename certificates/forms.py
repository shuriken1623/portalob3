from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        fields = ('last_name', 'first_name', 'middle_name', 'snils', 'position', 'department', 'power_of_attorney', 'certificate', 'certificate_expiration_date', 'is_terminated')
