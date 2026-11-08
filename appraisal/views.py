from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.db.models import Count, Avg, Q

from .models import (
    FacultyProfile,
    TeachingRecord,
    ResearchPublication,
    WorkshopTraining,
    CompletedProject,
    AppraisalSubmission,
)
from .forms import (
    FacultyProfileUpdateForm,
    TeachingRecordForm,
    ResearchPublicationForm,
    WorkshopTrainingForm,
    CompletedProjectForm,
    AppraisalSubmissionForm,
    AdminAppraisalReviewForm,
)
from .scoring import calculate_appraisal_score
from .pdf_generator import generate_appraisal_pdf


AVAILABLE_ACADEMIC_YEARS = ['2025-2026', '2024-2025', '2023-2024', '2022-2023']


# ---------------------------------------------------------------------------
# Access Control Decorators
# ---------------------------------------------------------------------------
def faculty_required(view_func):
    """Ensure user is logged in and has an associated faculty profile."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not hasattr(request.user, 'faculty_profile'):
            messages.error(request, "Access restricted to faculty members only.")
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return wrapper


def admin_required(view_func):
    """Ensure user is logged in and has staff or superuser privileges."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if not (request.user.is_staff or request.user.is_superuser):
            messages.error(request, "Access restricted to administrators only.")
            return redirect('dashboard_redirect')
        return view_func(request, *args, **kwargs)
    return wrapper


# ---------------------------------------------------------------------------
# FACULTY MODULE VIEWS
# ---------------------------------------------------------------------------

@faculty_required
def faculty_dashboard(request):
    profile = request.user.faculty_profile
    selected_year = request.GET.get('year', '2025-2026')
    if selected_year not in AVAILABLE_ACADEMIC_YEARS:
        selected_year = '2025-2026'

    # Fetch active submission for this academic year
    active_appraisal = AppraisalSubmission.objects.filter(
        faculty=profile,
        academic_year=selected_year
    ).first()

    # Pre-calculated dynamic score metrics
    score_data = calculate_appraisal_score(profile, selected_year)

    # Counts
    teaching_count = profile.teaching_records.filter(academic_year=selected_year).count()
    research_count = profile.research_publications.filter(academic_year=selected_year).count()
    workshop_count = profile.workshops_trainings.filter(academic_year=selected_year).count()
    project_count = profile.completed_projects.filter(academic_year=selected_year).count()

    context = {
        'profile': profile,
        'current_year': selected_year,
        'available_years': AVAILABLE_ACADEMIC_YEARS,
        'active_appraisal': active_appraisal,
        'score_data': score_data,
        'teaching_count': teaching_count,
        'research_count': research_count,
        'workshop_count': workshop_count,
        'project_count': project_count,
    }
    return render(request, 'faculty/dashboard.html', context)


@faculty_required
def faculty_profile_view(request):
    profile = request.user.faculty_profile
    return render(request, 'faculty/profile.html', {'profile': profile})


@faculty_required
def faculty_profile_update(request):
    profile = request.user.faculty_profile
    if request.method == 'POST':
        form = FacultyProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            # Update user names and email
            user = profile.user
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()

            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('faculty_profile')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = FacultyProfileUpdateForm(instance=profile)

    return render(request, 'faculty/profile_form.html', {'form': form, 'profile': profile})


# --- Teaching Records CRUD ---
@faculty_required
def teaching_list(request):
    profile = request.user.faculty_profile
    year_filter = request.GET.get('year', '').strip()
    records = profile.teaching_records.all()
    if year_filter:
        records = records.filter(academic_year=year_filter)
    return render(request, 'faculty/teaching_list.html', {
        'records': records,
        'year_filter': year_filter,
        'available_years': AVAILABLE_ACADEMIC_YEARS,
    })


@faculty_required
def teaching_create(request):
    profile = request.user.faculty_profile
    if request.method == 'POST':
        form = TeachingRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.faculty = profile
            record.save()
            messages.success(request, "Teaching record added successfully!")
            return redirect('teaching_list')
    else:
        form = TeachingRecordForm(initial={'academic_year': '2025-2026'})
    return render(request, 'faculty/teaching_form.html', {'form': form, 'title': 'Add Teaching Record'})


@faculty_required
def teaching_update(request, pk):
    profile = request.user.faculty_profile
    record = get_object_or_404(TeachingRecord, pk=pk, faculty=profile)
    if request.method == 'POST':
        form = TeachingRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Teaching record updated successfully!")
            return redirect('teaching_list')
    else:
        form = TeachingRecordForm(instance=record)
    return render(request, 'faculty/teaching_form.html', {'form': form, 'title': 'Edit Teaching Record', 'record': record})


@faculty_required
def teaching_delete(request, pk):
    profile = request.user.faculty_profile
    record = get_object_or_404(TeachingRecord, pk=pk, faculty=profile)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Teaching record deleted successfully.")
        return redirect('teaching_list')
    return render(request, 'faculty/confirm_delete.html', {'item': record, 'type': 'Teaching Record', 'back_url': 'teaching_list'})


# --- Research Publications CRUD ---
@faculty_required
def research_list(request):
    profile = request.user.faculty_profile
    year_filter = request.GET.get('year', '').strip()
    records = profile.research_publications.all()
    if year_filter:
        records = records.filter(academic_year=year_filter)
    return render(request, 'faculty/research_list.html', {
        'records': records,
        'year_filter': year_filter,
        'available_years': AVAILABLE_ACADEMIC_YEARS,
    })


@faculty_required
def research_create(request):
    profile = request.user.faculty_profile
    if request.method == 'POST':
        form = ResearchPublicationForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.faculty = profile
            record.save()
            messages.success(request, "Research publication added successfully!")
            return redirect('research_list')
    else:
        form = ResearchPublicationForm(initial={'academic_year': '2025-2026'})
    return render(request, 'faculty/research_form.html', {'form': form, 'title': 'Add Research Publication'})


@faculty_required
def research_update(request, pk):
    profile = request.user.faculty_profile
    record = get_object_or_404(ResearchPublication, pk=pk, faculty=profile)
    if request.method == 'POST':
        form = ResearchPublicationForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Research publication updated successfully!")
            return redirect('research_list')
    else:
        form = ResearchPublicationForm(instance=record)
    return render(request, 'faculty/research_form.html', {'form': form, 'title': 'Edit Research Publication', 'record': record})


@faculty_required
def research_delete(request, pk):
    profile = request.user.faculty_profile
    record = get_object_or_404(ResearchPublication, pk=pk, faculty=profile)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Research publication removed successfully.")
        return redirect('research_list')
    return render(request, 'faculty/confirm_delete.html', {'item': record, 'type': 'Research Publication', 'back_url': 'research_list'})


# --- Workshops & Training CRUD ---
@faculty_required
def workshop_list(request):
    profile = request.user.faculty_profile
    year_filter = request.GET.get('year', '').strip()
    records = profile.workshops_trainings.all()
    if year_filter:
        records = records.filter(academic_year=year_filter)
    return render(request, 'faculty/workshop_list.html', {
        'records': records,
        'year_filter': year_filter,
        'available_years': AVAILABLE_ACADEMIC_YEARS,
    })


@faculty_required
def workshop_create(request):
    profile = request.user.faculty_profile
    if request.method == 'POST':
        form = WorkshopTrainingForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.faculty = profile
            record.save()
            messages.success(request, "Workshop / Training record added successfully!")
            return redirect('workshop_list')
    else:
        form = WorkshopTrainingForm(initial={'academic_year': '2025-2026'})
    return render(request, 'faculty/workshop_form.html', {'form': form, 'title': 'Add Workshop / Training'})


@faculty_required
def workshop_update(request, pk):
    profile = request.user.faculty_profile
    record = get_object_or_404(WorkshopTraining, pk=pk, faculty=profile)
    if request.method == 'POST':
        form = WorkshopTrainingForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Workshop / Training updated successfully!")
            return redirect('workshop_list')
    else:
        form = WorkshopTrainingForm(instance=record)
    return render(request, 'faculty/workshop_form.html', {'form': form, 'title': 'Edit Workshop / Training', 'record': record})


@faculty_required
def workshop_delete(request, pk):
    profile = request.user.faculty_profile
    record = get_object_or_404(WorkshopTraining, pk=pk, faculty=profile)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Workshop record removed successfully.")
        return redirect('workshop_list')
    return render(request, 'faculty/confirm_delete.html', {'item': record, 'type': 'Workshop Record', 'back_url': 'workshop_list'})


# --- Completed Projects CRUD ---
@faculty_required
def project_list(request):
    profile = request.user.faculty_profile
    year_filter = request.GET.get('year', '').strip()
    records = profile.completed_projects.all()
    if year_filter:
        records = records.filter(academic_year=year_filter)
    return render(request, 'faculty/project_list.html', {
        'records': records,
        'year_filter': year_filter,
        'available_years': AVAILABLE_ACADEMIC_YEARS,
    })


@faculty_required
def project_create(request):
    profile = request.user.faculty_profile
    if request.method == 'POST':
        form = CompletedProjectForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.faculty = profile
            record.save()
            messages.success(request, "Project / Consultancy record added successfully!")
            return redirect('project_list')
    else:
        form = CompletedProjectForm(initial={'academic_year': '2025-2026'})
    return render(request, 'faculty/project_form.html', {'form': form, 'title': 'Add Project / Grant Record'})


@faculty_required
def project_update(request, pk):
    profile = request.user.faculty_profile
    record = get_object_or_404(CompletedProject, pk=pk, faculty=profile)
    if request.method == 'POST':
        form = CompletedProjectForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Project record updated successfully!")
            return redirect('project_list')
    else:
        form = CompletedProjectForm(instance=record)
    return render(request, 'faculty/project_form.html', {'form': form, 'title': 'Edit Project / Grant Record', 'record': record})


@faculty_required
def project_delete(request, pk):
    profile = request.user.faculty_profile
    record = get_object_or_404(CompletedProject, pk=pk, faculty=profile)
    if request.method == 'POST':
        record.delete()
        messages.success(request, "Project record removed successfully.")
        return redirect('project_list')
    return render(request, 'faculty/confirm_delete.html', {'item': record, 'type': 'Project Record', 'back_url': 'project_list'})


# --- Self-Appraisal Submission & Report ---
@faculty_required
def submit_appraisal(request):
    profile = request.user.faculty_profile
    academic_year = request.GET.get('year') or request.POST.get('academic_year') or '2025-2026'
    if academic_year not in AVAILABLE_ACADEMIC_YEARS:
        academic_year = '2025-2026'

    existing_submission = AppraisalSubmission.objects.filter(
        faculty=profile,
        academic_year=academic_year
    ).first()

    # If appraisal for this session is already approved and finalized, inform faculty
    if existing_submission and existing_submission.status == 'APPROVED' and request.method == 'GET':
        messages.info(
            request,
            f"Your self-appraisal for academic session {academic_year} is already approved and finalized."
        )
        return redirect('appraisal_detail', pk=existing_submission.pk)

    # Pre-calculated dynamic score for selected academic year
    score_breakdown = calculate_appraisal_score(profile, academic_year)

    if request.method == 'POST':
        form = AppraisalSubmissionForm(request.POST, instance=existing_submission)
        if form.is_valid():
            selected_form_year = form.cleaned_data['academic_year']

            # Duplicate protection: verify no conflict for another submission with this year
            conflict = AppraisalSubmission.objects.filter(
                faculty=profile,
                academic_year=selected_form_year
            )
            if existing_submission:
                conflict = conflict.exclude(pk=existing_submission.pk)

            if conflict.exists():
                messages.error(
                    request,
                    f"An appraisal submission for academic year {selected_form_year} already exists."
                )
                return redirect('appraisal_detail', pk=conflict.first().pk)

            # Recalculate score for selected form year to ensure full accuracy
            score_breakdown = calculate_appraisal_score(profile, selected_form_year)

            submission = form.save(commit=False)
            submission.faculty = profile
            submission.academic_year = selected_form_year
            submission.status = 'SUBMITTED'
            submission.teaching_score = score_breakdown['teaching_score']
            submission.research_score = score_breakdown['research_score']
            submission.workshop_score = score_breakdown['workshop_score']
            submission.project_score = score_breakdown['project_score']
            submission.total_score = score_breakdown['total_score']
            submission.performance_grade = score_breakdown['performance_grade']
            submission.promotion_recommendation = score_breakdown['promotion_recommendation']
            submission.save()

            messages.success(
                request,
                f"Self-Appraisal for {selected_form_year} submitted successfully! Calculated Performance Score: {submission.total_score} / 100 ({submission.performance_grade})."
            )
            return redirect('appraisal_detail', pk=submission.pk)
        else:
            messages.error(request, "Please correct the errors in the appraisal submission form.")
    else:
        form = AppraisalSubmissionForm(
            instance=existing_submission,
            initial={'academic_year': academic_year}
        )

    teaching_records = profile.teaching_records.filter(academic_year=academic_year)
    research_records = profile.research_publications.filter(academic_year=academic_year)
    workshop_records = profile.workshops_trainings.filter(academic_year=academic_year)
    project_records = profile.completed_projects.filter(academic_year=academic_year)

    context = {
        'profile': profile,
        'academic_year': academic_year,
        'available_years': AVAILABLE_ACADEMIC_YEARS,
        'score_breakdown': score_breakdown,
        'existing_submission': existing_submission,
        'form': form,
        'teaching_records': teaching_records,
        'research_records': research_records,
        'workshop_records': workshop_records,
        'project_records': project_records,
    }
    return render(request, 'faculty/submit_appraisal.html', context)


@faculty_required
def appraisal_detail(request, pk):
    profile = request.user.faculty_profile
    appraisal = get_object_or_404(AppraisalSubmission, pk=pk, faculty=profile)
    return render(request, 'faculty/appraisal_detail.html', {'appraisal': appraisal})


@faculty_required
def download_appraisal_pdf(request, pk):
    profile = request.user.faculty_profile
    appraisal = get_object_or_404(AppraisalSubmission, pk=pk, faculty=profile)
    pdf_buffer = generate_appraisal_pdf(appraisal)
    filename = f"Appraisal_{profile.employee_id}_{appraisal.academic_year}.pdf"
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


# ---------------------------------------------------------------------------
# ADMIN MODULE VIEWS
# ---------------------------------------------------------------------------

@admin_required
def admin_dashboard(request):
    current_year = request.GET.get('year', '2025-2026')
    if current_year not in AVAILABLE_ACADEMIC_YEARS:
        current_year = '2025-2026'

    total_faculty = FacultyProfile.objects.count()
    total_appraisals = AppraisalSubmission.objects.filter(academic_year=current_year).count()
    pending_appraisals = AppraisalSubmission.objects.filter(
        academic_year=current_year,
        status__in=['SUBMITTED', 'UNDER_REVIEW']
    ).count()
    approved_appraisals = AppraisalSubmission.objects.filter(
        academic_year=current_year,
        status='APPROVED'
    ).count()
    promotion_eligible = FacultyProfile.objects.filter(
        promotion_status__in=['Eligible for Promotion', 'Promoted']
    ).count()

    # Department breakdown for Chart.js
    dept_counts = (
        FacultyProfile.objects.values('department')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    dept_labels = [dict(FacultyProfile.DEPARTMENT_CHOICES).get(d['department'], d['department']) for d in dept_counts]
    dept_data = [d['total'] for d in dept_counts]

    # Status breakdown for Chart.js
    status_counts = (
        AppraisalSubmission.objects.filter(academic_year=current_year)
        .values('status')
        .annotate(total=Count('id'))
    )
    status_dict = {s['status']: s['total'] for s in status_counts}
    status_labels = ['Approved', 'Submitted / Pending', 'Under Review', 'Revision Requested', 'Rejected']
    status_data = [
        status_dict.get('APPROVED', 0),
        status_dict.get('SUBMITTED', 0),
        status_dict.get('UNDER_REVIEW', 0),
        status_dict.get('REVISION_REQUESTED', 0),
        status_dict.get('REJECTED', 0),
    ]

    recent_submissions = (
        AppraisalSubmission.objects.select_related('faculty', 'faculty__user')
        .order_by('-submission_date')[:6]
    )

    context = {
        'total_faculty': total_faculty,
        'total_appraisals': total_appraisals,
        'pending_appraisals': pending_appraisals,
        'approved_appraisals': approved_appraisals,
        'promotion_eligible': promotion_eligible,
        'recent_submissions': recent_submissions,
        'current_year': current_year,
        'available_years': AVAILABLE_ACADEMIC_YEARS,
        'dept_labels': dept_labels,
        'dept_data': dept_data,
        'status_labels': status_labels,
        'status_data': status_data,
    }
    return render(request, 'admin_portal/dashboard.html', context)


@admin_required
def admin_faculty_list(request):
    profiles = FacultyProfile.objects.select_related('user').all()

    # Search & filters
    search_query = request.GET.get('q', '').strip()
    dept_filter = request.GET.get('department', '').strip()
    status_filter = request.GET.get('promotion_status', '').strip()

    if search_query:
        profiles = profiles.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(user__email__icontains=search_query)
        )

    if dept_filter:
        profiles = profiles.filter(department=dept_filter)

    if status_filter:
        profiles = profiles.filter(promotion_status=status_filter)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'dept_filter': dept_filter,
        'status_filter': status_filter,
        'department_choices': FacultyProfile.DEPARTMENT_CHOICES,
        'promotion_choices': FacultyProfile.PROMOTION_STATUS_CHOICES,
    }
    return render(request, 'admin_portal/faculty_list.html', context)


@admin_required
def admin_faculty_detail(request, pk):
    profile = get_object_or_404(FacultyProfile.objects.select_related('user'), pk=pk)
    teaching_records = profile.teaching_records.all()
    research_records = profile.research_publications.all()
    workshop_records = profile.workshops_trainings.all()
    project_records = profile.completed_projects.all()
    appraisals = profile.appraisals.all()

    context = {
        'profile': profile,
        'teaching_records': teaching_records,
        'research_records': research_records,
        'workshop_records': workshop_records,
        'project_records': project_records,
        'appraisals': appraisals,
    }
    return render(request, 'admin_portal/faculty_detail.html', context)


@admin_required
def admin_appraisals_list(request):
    appraisals = AppraisalSubmission.objects.select_related('faculty', 'faculty__user').all()

    status_filter = request.GET.get('status', '').strip()
    year_filter = request.GET.get('year', '').strip()

    if status_filter:
        appraisals = appraisals.filter(status=status_filter)

    if year_filter:
        appraisals = appraisals.filter(academic_year=year_filter)

    context = {
        'appraisals': appraisals,
        'status_filter': status_filter,
        'year_filter': year_filter,
        'status_choices': AppraisalSubmission.STATUS_CHOICES,
    }
    return render(request, 'admin_portal/appraisals_list.html', context)


@admin_required
def admin_appraisal_review(request, pk):
    appraisal = get_object_or_404(
        AppraisalSubmission.objects.select_related('faculty', 'faculty__user'),
        pk=pk
    )
    profile = appraisal.faculty

    if request.method == 'POST':
        form = AdminAppraisalReviewForm(request.POST, instance=appraisal)
        if form.is_valid():
            appraisal = form.save(commit=False)
            appraisal.reviewed_by = request.user
            appraisal.reviewed_at = timezone.now()
            appraisal.save()

            # Update the faculty's promotion status
            new_promo_status = form.cleaned_data['promotion_status']
            profile.promotion_status = new_promo_status
            if new_promo_status in ['Eligible for Promotion', 'Promoted']:
                profile.promotion_eligible_date = timezone.now().date()
            profile.save()

            messages.success(
                request,
                f"Appraisal review for {profile.user.get_full_name() or profile.employee_id} saved. Status: {appraisal.get_status_display()}."
            )
            return redirect('admin_appraisals_list')
    else:
        form = AdminAppraisalReviewForm(
            instance=appraisal,
            initial={'promotion_status': profile.promotion_status}
        )

    # Fetch all records for the appraisal's academic year
    teaching_records = profile.teaching_records.filter(academic_year=appraisal.academic_year)
    research_records = profile.research_publications.filter(academic_year=appraisal.academic_year)
    workshop_records = profile.workshops_trainings.filter(academic_year=appraisal.academic_year)
    project_records = profile.completed_projects.filter(academic_year=appraisal.academic_year)

    context = {
        'appraisal': appraisal,
        'profile': profile,
        'form': form,
        'teaching_records': teaching_records,
        'research_records': research_records,
        'workshop_records': workshop_records,
        'project_records': project_records,
    }
    return render(request, 'admin_portal/appraisal_review.html', context)


@admin_required
def admin_update_promotion(request, pk):
    profile = get_object_or_404(FacultyProfile, pk=pk)
    if request.method == 'POST':
        status = request.POST.get('promotion_status')
        if status in dict(FacultyProfile.PROMOTION_STATUS_CHOICES):
            profile.promotion_status = status
            if status in ['Eligible for Promotion', 'Promoted']:
                profile.promotion_eligible_date = timezone.now().date()
            profile.save()
            messages.success(request, f"Promotion status for {profile.employee_id} updated to '{status}'.")
        else:
            messages.error(request, "Invalid promotion status selected.")
    return redirect('admin_faculty_detail', pk=profile.pk)


@admin_required
def admin_download_pdf(request, pk):
    appraisal = get_object_or_404(AppraisalSubmission, pk=pk)
    pdf_buffer = generate_appraisal_pdf(appraisal)
    filename = f"Faculty_Appraisal_{appraisal.faculty.employee_id}_{appraisal.academic_year}.pdf"
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


@admin_required
def admin_export_appraisals_csv(request):
    """
    Exports summary of all appraisal submissions to CSV for committee meetings.
    """
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Faculty_Appraisals_Summary.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Employee ID', 'Faculty Name', 'Department', 'Designation',
        'Academic Session', 'Teaching Score (/40)', 'Research Score (/30)',
        'Workshop Score (/15)', 'Project Score (/15)', 'Total Score (/100)',
        'Performance Grade', 'Review Status', 'CAS Recommendation',
        'Submission Date', 'Reviewed On'
    ])

    appraisals = AppraisalSubmission.objects.select_related('faculty', 'faculty__user').all()
    for a in appraisals:
        writer.writerow([
            a.faculty.employee_id,
            a.faculty.user.get_full_name() or a.faculty.user.username,
            a.faculty.get_department_display(),
            a.faculty.designation,
            a.academic_year,
            a.teaching_score,
            a.research_score,
            a.workshop_score,
            a.project_score,
            a.total_score,
            a.performance_grade,
            a.get_status_display(),
            a.promotion_recommendation,
            a.submission_date.strftime('%Y-%m-%d %H:%M'),
            a.reviewed_at.strftime('%Y-%m-%d %H:%M') if a.reviewed_at else 'Pending'
        ])

    return response


@admin_required
def admin_export_faculty_csv(request):
    """
    Exports faculty directory to CSV.
    """
    import csv
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Faculty_Directory.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Employee ID', 'Faculty Name', 'Email', 'Department', 'Designation',
        'Highest Qualification', 'Specialization', 'Date of Joining',
        'Experience (Years)', 'Contact Phone', 'Promotion Status', 'Eligibility Date'
    ])

    profiles = FacultyProfile.objects.select_related('user').all()
    for p in profiles:
        writer.writerow([
            p.employee_id,
            p.user.get_full_name() or p.user.username,
            p.user.email,
            p.get_department_display(),
            p.designation,
            p.highest_qualification,
            p.specialization,
            str(p.date_of_joining),
            p.experience_years,
            p.contact_number,
            p.promotion_status,
            str(p.promotion_eligible_date) if p.promotion_eligible_date else 'N/A'
        ])

    return response

