from django.contrib import admin
from .models import (
    FacultyProfile,
    TeachingRecord,
    ResearchPublication,
    WorkshopTraining,
    CompletedProject,
    AppraisalSubmission,
)


@admin.register(FacultyProfile)
class FacultyProfileAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'department', 'designation', 'highest_qualification', 'experience_years', 'promotion_status')
    list_filter = ('department', 'designation', 'promotion_status')
    search_fields = ('employee_id', 'user__username', 'user__first_name', 'user__last_name', 'specialization')


@admin.register(TeachingRecord)
class TeachingRecordAdmin(admin.ModelAdmin):
    list_display = ('subject_code', 'subject_name', 'faculty', 'academic_year', 'semester', 'scheduled_hours', 'conducted_hours', 'pass_percentage')
    list_filter = ('academic_year', 'semester', 'course_type')
    search_fields = ('subject_code', 'subject_name', 'faculty__employee_id')


@admin.register(ResearchPublication)
class ResearchPublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty', 'publication_type', 'journal_conference_name', 'publication_date', 'author_role')
    list_filter = ('publication_type', 'academic_year', 'author_role')
    search_fields = ('title', 'journal_conference_name', 'faculty__employee_id', 'issn_isbn')


@admin.register(WorkshopTraining)
class WorkshopTrainingAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty', 'program_type', 'role', 'organizing_institution', 'duration_days', 'start_date')
    list_filter = ('program_type', 'role', 'academic_year')
    search_fields = ('title', 'organizing_institution', 'faculty__employee_id')


@admin.register(CompletedProject)
class CompletedProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'faculty', 'funding_agency', 'project_type', 'grant_amount', 'role', 'status')
    list_filter = ('project_type', 'role', 'status', 'academic_year')
    search_fields = ('title', 'funding_agency', 'faculty__employee_id')


@admin.register(AppraisalSubmission)
class AppraisalSubmissionAdmin(admin.ModelAdmin):
    list_display = ('faculty', 'academic_year', 'status', 'total_score', 'performance_grade', 'promotion_recommendation', 'submission_date')
    list_filter = ('status', 'academic_year', 'performance_grade', 'promotion_recommendation')
    search_fields = ('faculty__employee_id', 'faculty__user__first_name', 'faculty__user__last_name')
