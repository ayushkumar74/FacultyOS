from django import forms
from .models import (
    FacultyProfile,
    TeachingRecord,
    ResearchPublication,
    WorkshopTraining,
    CompletedProject,
    AppraisalSubmission,
)


ACADEMIC_YEAR_CHOICES = [
    ('2025-2026', '2025-2026 (Current Academic Session)'),
    ('2024-2025', '2024-2025'),
    ('2023-2024', '2023-2024'),
    ('2022-2023', '2022-2023'),
]


class FacultyProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = FacultyProfile
        fields = [
            'department',
            'designation',
            'highest_qualification',
            'specialization',
            'date_of_joining',
            'experience_years',
            'contact_number',
            'address',
        ]
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select'}),
            'designation': forms.Select(attrs={'class': 'form-select'}),
            'highest_qualification': forms.Select(attrs={'class': 'form-select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_joining': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email


class TeachingRecordForm(forms.ModelForm):
    academic_year = forms.ChoiceField(
        choices=ACADEMIC_YEAR_CHOICES,
        initial='2025-2026',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = TeachingRecord
        fields = [
            'academic_year',
            'semester',
            'subject_name',
            'subject_code',
            'course_type',
            'scheduled_hours',
            'conducted_hours',
            'pass_percentage',
            'student_feedback_score',
            'innovative_teaching_methods',
        ]
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-select'}),
            'subject_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Data Structures & Algorithms'}),
            'subject_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CS-301'}),
            'course_type': forms.Select(attrs={'class': 'form-select'}),
            'scheduled_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 60'}),
            'conducted_hours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 58'}),
            'pass_percentage': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g. 94.50'}),
            'student_feedback_score': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g. 4.65 (out of 5.00)'}),
            'innovative_teaching_methods': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. Active learning, interactive coding, Google Classroom assignments'}),
        }


class ResearchPublicationForm(forms.ModelForm):
    academic_year = forms.ChoiceField(
        choices=ACADEMIC_YEAR_CHOICES,
        initial='2025-2026',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = ResearchPublication
        fields = [
            'academic_year',
            'title',
            'journal_conference_name',
            'publication_type',
            'issn_isbn',
            'publication_date',
            'indexing_details',
            'author_role',
            'doi_or_url',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Paper title'}),
            'journal_conference_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Journal or Conference name'}),
            'publication_type': forms.Select(attrs={'class': 'form-select'}),
            'issn_isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ISSN 1234-5678'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'indexing_details': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. SCI Impact Factor 4.5, Scopus Q1'}),
            'author_role': forms.Select(attrs={'class': 'form-select'}),
            'doi_or_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://doi.org/10.xxxx/xxxx'}),
        }


class WorkshopTrainingForm(forms.ModelForm):
    academic_year = forms.ChoiceField(
        choices=ACADEMIC_YEAR_CHOICES,
        initial='2025-2026',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = WorkshopTraining
        fields = [
            'academic_year',
            'title',
            'program_type',
            'role',
            'organizing_institution',
            'start_date',
            'end_date',
            'duration_days',
            'certificate_link',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Program title'}),
            'program_type': forms.Select(attrs={'class': 'form-select'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'organizing_institution': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. IIT Delhi, AICTE ATAL Academy'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'certificate_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Optional URL to certificate'}),
        }


class CompletedProjectForm(forms.ModelForm):
    academic_year = forms.ChoiceField(
        choices=ACADEMIC_YEAR_CHOICES,
        initial='2025-2026',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = CompletedProject
        fields = [
            'academic_year',
            'title',
            'funding_agency',
            'project_type',
            'grant_amount',
            'duration_months',
            'role',
            'status',
            'completion_date',
            'outcomes_summary',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'funding_agency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. DST-SERB, AICTE, Tech Mahindra'}),
            'project_type': forms.Select(attrs={'class': 'form-select'}),
            'grant_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '1000', 'placeholder': 'e.g. 750000.00'}),
            'duration_months': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'placeholder': 'e.g. 24'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'outcomes_summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Key outcomes, publications, patents, prototypes'}),
        }


class AppraisalSubmissionForm(forms.ModelForm):
    academic_year = forms.ChoiceField(
        choices=ACADEMIC_YEAR_CHOICES,
        initial='2025-2026',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'academicYearSelect'})
    )

    class Meta:
        model = AppraisalSubmission
        fields = ['academic_year', 'faculty_remarks']
        widgets = {
            'faculty_remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Provide a summary of your achievements, innovations, student mentorship, and goals for the next academic year...'
            }),
        }


class AdminAppraisalReviewForm(forms.ModelForm):
    promotion_status = forms.ChoiceField(
        choices=FacultyProfile.PROMOTION_STATUS_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = AppraisalSubmission
        fields = ['status', 'promotion_recommendation', 'admin_remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'promotion_recommendation': forms.Select(attrs={'class': 'form-select'}),
            'admin_remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter review feedback, evaluation committee notes, commendations or revision instructions...'
            }),
        }

