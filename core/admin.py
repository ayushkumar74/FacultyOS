from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from appraisal.models import FacultyProfile


class FacultyProfileInline(admin.StackedInline):
    model = FacultyProfile
    can_delete = False
    verbose_name_plural = 'Faculty Profile'
    fk_name = 'user'
    extra = 0


class UserAdmin(BaseUserAdmin):
    inlines = (FacultyProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_employee_id', 'get_department')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    def get_employee_id(self, instance):
        if hasattr(instance, 'faculty_profile'):
            return instance.faculty_profile.employee_id
        return '-'
    get_employee_id.short_description = 'Employee ID'

    def get_department(self, instance):
        if hasattr(instance, 'faculty_profile'):
            return instance.faculty_profile.get_department_display()
        return '-'
    get_department.short_description = 'Department'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
