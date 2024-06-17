from django.contrib import admin
from .models import Position, Department, PowerOfAttorney, Certificate, Employee

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'position', 'department')
    list_filter = ('position', 'department')
    search_fields = ('last_name', 'first_name', 'middle_name', 'snils')

admin.site.register(Position)
admin.site.register(Department)
admin.site.register(PowerOfAttorney)
admin.site.register(Certificate)
admin.site.register(Employee, EmployeeAdmin)

