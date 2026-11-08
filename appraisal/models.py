from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class FacultyProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics & Communication Engineering'),
        ('EEE', 'Electrical & Electronics Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('MGMT', 'Management Studies'),
        ('BSH', 'Basic Sciences & Humanities'),
    ]

    DESIGNATION_CHOICES = [
        ('Assistant Professor', 'Assistant Professor'),
        ('Associate Professor', 'Associate Professor'),
        ('Professor', 'Professor'),
        ('Senior Professor', 'Senior Professor'),
        ('Head of Department', 'Head of Department'),
    ]

    QUALIFICATION_CHOICES = [
        ('Ph.D.', 'Doctor of Philosophy (Ph.D.)'),
        ('M.Tech / M.E.', 'Master of Technology / Engineering'),
        ('M.Sc.', 'Master of Science'),
        ('MBA', 'Master of Business Administration'),
        ('M.Phil', 'Master of Philosophy'),
        ('B.Tech / B.E.', 'Bachelor of Technology / Engineering'),
    ]

    PROMOTION_STATUS_CHOICES = [
        ('Not Applied', 'Not Applied'),
        ('Under Review', 'Under Review'),
        ('Eligible for Promotion', 'Eligible for Promotion'),
        ('Promoted', 'Promoted'),
        ('Not Eligible', 'Not Eligible'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='faculty_profile')
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Faculty / Employee ID")
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='CSE')
    designation = models.CharField(max_length=50, choices=DESIGNATION_CHOICES, default='Assistant Professor')
    highest_qualification = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES, default='M.Tech / M.E.')
    specialization = models.CharField(max_length=150, help_text="Area of expertise/specialization")
    date_of_joining = models.DateField(default=timezone.now)
    experience_years = models.DecimalField(max_digits=4, decimal_places=1, default=1.0, help_text="Total teaching experience in years")
    contact_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    promotion_status = models.CharField(max_length=30, choices=PROMOTION_STATUS_CHOICES, default='Not Applied')
    promotion_eligible_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee_id']
        verbose_name = "Faculty Profile"
        verbose_name_plural = "Faculty Profiles"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.employee_id}) - {self.get_department_display()}"


class TeachingRecord(models.Model):
    SEMESTER_CHOICES = [
        ('Odd', 'Odd Semester (Sem 1, 3, 5, 7)'),
        ('Even', 'Even Semester (Sem 2, 4, 6, 8)'),
    ]

    COURSE_TYPE_CHOICES = [
        ('Theory', 'Theory Lecture'),
        ('Practical', 'Practical / Laboratory'),
        ('Project', 'Project / Seminar Mentorship'),
    ]

    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='teaching_records')
    academic_year = models.CharField(max_length=20, default='2025-2026', help_text="e.g. 2025-2026")
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES, default='Odd')
    subject_name = models.CharField(max_length=120)
    subject_code = models.CharField(max_length=30)
    course_type = models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES, default='Theory')
    scheduled_hours = models.PositiveIntegerField(help_text="Total scheduled lecture/lab hours")
    conducted_hours = models.PositiveIntegerField(help_text="Total classes conducted")
    pass_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Student pass percentage (0-100%)"
    )
    student_feedback_score = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],
        help_text="Student feedback rating out of 5.00"
    )
    innovative_teaching_methods = models.TextField(blank=True, help_text="ICT tools, flipped classroom, problem-based learning, etc.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-academic_year', 'semester', 'subject_code']
        verbose_name = "Teaching Record"
        verbose_name_plural = "Teaching Records"

    def __str__(self):
        return f"{self.subject_code} - {self.subject_name} ({self.academic_year})"

    @property
    def compliance_rate(self):
        if self.scheduled_hours > 0:
            return round((self.conducted_hours / self.scheduled_hours) * 100, 1)
        return 0.0


class ResearchPublication(models.Model):
    PUB_TYPE_CHOICES = [
        ('SCI_SCOPUS', 'SCI / Scopus Indexed Journal (High Impact)'),
        ('UGC_CARE', 'UGC-CARE / Peer-Reviewed Refereed Journal'),
        ('INT_CONF', 'International IEEE/Springer/ACM Conference'),
        ('NAT_CONF', 'National Conference / Symposium'),
        ('BOOK_CHAPTER', 'Book / Edited Book Chapter (with ISBN)'),
        ('PATENT', 'Patent (Published / Granted)'),
    ]

    AUTHOR_ROLE_CHOICES = [
        ('First Author', 'First Author / Primary Researcher'),
        ('Corresponding Author', 'Corresponding Author'),
        ('Co-Author', 'Co-Author / Contributing Member'),
    ]

    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='research_publications')
    academic_year = models.CharField(max_length=20, default='2025-2026', help_text="e.g. 2025-2026")
    title = models.CharField(max_length=255, verbose_name="Publication / Paper Title")
    journal_conference_name = models.CharField(max_length=255, verbose_name="Journal / Conference / Publisher Name")
    publication_type = models.CharField(max_length=20, choices=PUB_TYPE_CHOICES, default='SCI_SCOPUS')
    issn_isbn = models.CharField(max_length=50, blank=True, verbose_name="ISSN / ISBN Number")
    publication_date = models.DateField(default=timezone.now)
    indexing_details = models.CharField(max_length=100, blank=True, help_text="e.g. Scopus Q1, Web of Science, IF 4.2")
    author_role = models.CharField(max_length=30, choices=AUTHOR_ROLE_CHOICES, default='First Author')
    doi_or_url = models.URLField(blank=True, verbose_name="DOI / Paper Web Link")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-publication_date']
        verbose_name = "Research Publication"
        verbose_name_plural = "Research Publications"

    def __str__(self):
        return f"{self.title[:60]}... ({self.academic_year})"


class WorkshopTraining(models.Model):
    PROGRAM_TYPE_CHOICES = [
        ('FDP', 'Faculty Development Program (FDP) - 1/2 Weeks'),
        ('STTP', 'Short Term Training Program (STTP)'),
        ('WORKSHOP', 'Hands-on Technical Workshop'),
        ('ORIENTATION', 'Orientation / Refresher Course (HRDC/AICTE)'),
        ('SEMINAR', 'National / International Seminar or Webinar'),
    ]

    ROLE_CHOICES = [
        ('Participant', 'Active Participant / Attendee'),
        ('Resource Person', 'Resource Person / Keynote Speaker'),
        ('Coordinator', 'Program Coordinator / Organizer'),
    ]

    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='workshops_trainings')
    academic_year = models.CharField(max_length=20, default='2025-2026', help_text="e.g. 2025-2026")
    title = models.CharField(max_length=255, verbose_name="Workshop / Training Title")
    program_type = models.CharField(max_length=20, choices=PROGRAM_TYPE_CHOICES, default='FDP')
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='Participant')
    organizing_institution = models.CharField(max_length=200, help_text="IIT, NIT, University, Industry Partner, etc.")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(default=timezone.now)
    duration_days = models.PositiveIntegerField(default=5, help_text="Duration in days")
    certificate_link = models.URLField(blank=True, help_text="Link to verification certificate or folder")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Workshop & Training Record"
        verbose_name_plural = "Workshops & Training Records"

    def __str__(self):
        return f"{self.title[:60]} ({self.get_program_type_display()})"


class CompletedProject(models.Model):
    PROJECT_TYPE_CHOICES = [
        ('RESEARCH_GRANT', 'Sponsored Research Grant (Govt/DST/AICTE)'),
        ('CONSULTANCY', 'Industrial Consultancy Project'),
        ('INSTITUTIONAL', 'Institutional / Modernization Grant (MODROBS)'),
        ('STUDENT_MENTOR', 'Major Student Capstone / Incubation Mentorship'),
    ]

    ROLE_CHOICES = [
        ('PI', 'Principal Investigator (PI)'),
        ('CO_PI', 'Co-Principal Investigator (Co-PI)'),
        ('LEAD', 'Project Consultant / Lead'),
    ]

    STATUS_CHOICES = [
        ('Completed', 'Completed'),
        ('Ongoing', 'Ongoing / In Progress'),
    ]

    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='completed_projects')
    academic_year = models.CharField(max_length=20, default='2025-2026', help_text="e.g. 2025-2026")
    title = models.CharField(max_length=255, verbose_name="Project Title")
    funding_agency = models.CharField(max_length=150, help_text="e.g. DST-SERB, AICTE, UGC, Industry Sponsor")
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPE_CHOICES, default='RESEARCH_GRANT')
    grant_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Grant amount in INR (e.g. 500000.00)")
    duration_months = models.PositiveIntegerField(default=12, help_text="Project duration in months")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PI')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Completed')
    completion_date = models.DateField(null=True, blank=True)
    outcomes_summary = models.TextField(blank=True, help_text="Patents, prototypes, lab upgrades, publications generated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-academic_year', '-created_at']
        verbose_name = "Sponsored Project / Consultancy"
        verbose_name_plural = "Sponsored Projects & Consultancies"

    def __str__(self):
        return f"{self.title[:60]} ({self.funding_agency})"


class AppraisalSubmission(models.Model):
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('SUBMITTED', 'Submitted for Review'),
        ('UNDER_REVIEW', 'Under Review'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('REVISION_REQUESTED', 'Revision Requested'),
    ]

    PROMOTION_REC_CHOICES = [
        ('Recommended for Promotion', 'Recommended for Promotion'),
        ('Eligible - Promotion Awarded', 'Eligible - Promotion Awarded'),
        ('Deferred / Under Review', 'Deferred / Under Review'),
        ('Not Recommended', 'Not Recommended at this stage'),
        ('Not Applicable', 'Not Applicable'),
    ]

    faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE, related_name='appraisals')
    academic_year = models.CharField(max_length=20, default='2025-2026')
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='SUBMITTED')

    # Pre-calculated automated performance evaluation scores
    teaching_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Max 40 points")
    research_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Max 30 points")
    workshop_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Max 15 points")
    project_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Max 15 points")
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0.0, help_text="Max 100 points")
    performance_grade = models.CharField(max_length=50, default='Good (B)')

    faculty_remarks = models.TextField(blank=True, help_text="Faculty self-reflection, major achievements, roadmap")
    admin_remarks = models.TextField(blank=True, help_text="Reviewer / Committee comments, recommendations, instructions")
    promotion_recommendation = models.CharField(
        max_length=50,
        choices=PROMOTION_REC_CHOICES,
        default='Deferred / Under Review'
    )
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_appraisals')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-academic_year', '-submission_date']
        unique_together = ('faculty', 'academic_year')
        verbose_name = "Self-Appraisal Submission"
        verbose_name_plural = "Self-Appraisal Submissions"

    def __str__(self):
        return f"Appraisal {self.academic_year} - {self.faculty.employee_id} ({self.status})"
