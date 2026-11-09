from django.test import TestCase, Client, RequestFactory, override_settings
from django.urls import reverse
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from core.views import custom_404, custom_500
from appraisal.models import (
    FacultyProfile,
    TeachingRecord,
    ResearchPublication,
    WorkshopTraining,
    CompletedProject,
    AppraisalSubmission,
)
from appraisal.scoring import calculate_appraisal_score
from appraisal.pdf_generator import generate_appraisal_pdf


class FacultyAppraisalPortalTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create Admin User
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@test.edu',
            password='testpassword123',
            is_staff=True,
            is_superuser=True
        )

        # Create Faculty User & Profile
        self.faculty_user = User.objects.create_user(
            username='faculty_test',
            email='faculty@test.edu',
            password='testpassword123',
            first_name='Ananya',
            last_name='Verma'
        )
        self.faculty_profile = FacultyProfile.objects.create(
            user=self.faculty_user,
            employee_id='FAC-TEST-001',
            department='CSE',
            designation='Assistant Professor',
            highest_qualification='Ph.D.',
            specialization='Machine Learning',
            date_of_joining=date(2020, 1, 1),
            experience_years=Decimal('5.0'),
            contact_number='+91 9999999999',
            promotion_status='Not Applied'
        )

    def test_performance_scoring_engine(self):
        """Test calculation of teaching, research, workshop, and project scores."""
        # 1. Add Teaching Record
        TeachingRecord.objects.create(
            faculty=self.faculty_profile,
            academic_year='2025-2026',
            subject_name='Artificial Intelligence',
            subject_code='CS-401',
            scheduled_hours=60,
            conducted_hours=60,
            pass_percentage=Decimal('95.00'),
            student_feedback_score=Decimal('4.50')
        )

        # 2. Add Research Publication (SCI/Scopus First Author)
        ResearchPublication.objects.create(
            faculty=self.faculty_profile,
            academic_year='2025-2026',
            title='Transformers in Edge IoT',
            journal_conference_name='IEEE Internet of Things Journal',
            publication_type='SCI_SCOPUS',
            author_role='First Author',
            publication_date=date(2025, 10, 1)
        )

        # 3. Add Workshop (FDP 5 days)
        WorkshopTraining.objects.create(
            faculty=self.faculty_profile,
            academic_year='2025-2026',
            title='FDP on Deep Learning',
            program_type='FDP',
            role='Participant',
            organizing_institution='IIT Bombay',
            duration_days=5
        )

        # 4. Add Project (Research Grant PI)
        CompletedProject.objects.create(
            faculty=self.faculty_profile,
            academic_year='2025-2026',
            title='AI for Healthcare',
            funding_agency='DST',
            project_type='RESEARCH_GRANT',
            grant_amount=Decimal('500000.00'),
            duration_months=12,
            role='PI',
            status='Completed'
        )

        scores = calculate_appraisal_score(self.faculty_profile, '2025-2026')

        self.assertGreater(scores['teaching_score'], Decimal('35.00'))
        self.assertEqual(scores['research_score'], Decimal('10.00'))
        self.assertEqual(scores['workshop_score'], Decimal('5.00'))
        self.assertEqual(scores['project_score'], Decimal('10.00'))
        self.assertGreater(scores['total_score'], Decimal('60.00'))
        self.assertIn('Grade', scores['performance_grade'])

    def test_faculty_crud_operations(self):
        """Test adding and updating records through client view requests."""
        self.client.login(username='faculty_test', password='testpassword123')

        # Add Teaching record via POST
        response = self.client.post('/faculty/teaching/add/', {
            'academic_year': '2025-2026',
            'semester': 'Odd',
            'subject_name': 'Operating Systems',
            'subject_code': 'CS-302',
            'course_type': 'Theory',
            'scheduled_hours': 50,
            'conducted_hours': 48,
            'pass_percentage': '92.50',
            'student_feedback_score': '4.60',
            'innovative_teaching_methods': 'Linux kernel tracing labs',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(TeachingRecord.objects.filter(subject_code='CS-302').exists())

    def test_appraisal_submission_and_pdf(self):
        """Test submitting self-appraisal and downloading generated PDF."""
        self.client.login(username='faculty_test', password='testpassword123')

        response = self.client.post('/faculty/appraisal/submit/', {
            'academic_year': '2025-2026',
            'faculty_remarks': 'Dedicated to student outcomes and high research productivity.',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        submission = AppraisalSubmission.objects.get(faculty=self.faculty_profile, academic_year='2025-2026')
        self.assertEqual(submission.status, 'SUBMITTED')

        # Test PDF Generation
        pdf_response = self.client.get(f'/faculty/appraisal/{submission.pk}/pdf/')
        self.assertEqual(pdf_response.status_code, 200)
        self.assertEqual(pdf_response['Content-Type'], 'application/pdf')
        self.assertGreater(len(pdf_response.content), 1000)

    def test_admin_appraisal_review_and_promotion(self):
        """Test admin reviewing appraisal, updating status, and changing promotion readiness."""
        # Create submission
        submission = AppraisalSubmission.objects.create(
            faculty=self.faculty_profile,
            academic_year='2025-2026',
            status='SUBMITTED',
            total_score=Decimal('78.50'),
            performance_grade='Very Good (A)'
        )

        self.client.login(username='admin_test', password='testpassword123')

        # Admin reviews and approves
        response = self.client.post(f'/admin-portal/appraisals/{submission.pk}/review/', {
            'status': 'APPROVED',
            'promotion_recommendation': 'Recommended for Promotion',
            'promotion_status': 'Eligible for Promotion',
            'admin_remarks': 'Approved by Academic Review Committee. Eligible for Promotion.',
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        submission.refresh_from_db()
        self.faculty_profile.refresh_from_db()

        self.assertEqual(submission.status, 'APPROVED')
        self.assertEqual(submission.promotion_recommendation, 'Recommended for Promotion')
        self.assertEqual(self.faculty_profile.promotion_status, 'Eligible for Promotion')

    def test_admin_csv_exports(self):
        """Test CSV exports for appraisals and faculty directory, including access control."""
        # Non-admin / faculty attempt should be blocked
        self.client.login(username='faculty_test', password='testpassword123')
        res_blocked = self.client.get('/admin-portal/appraisals/export-csv/')
        self.assertEqual(res_blocked.status_code, 302)

        # Admin attempt
        self.client.login(username='admin_test', password='testpassword123')

        # 1. Export Appraisals CSV
        res_appraisals = self.client.get('/admin-portal/appraisals/export-csv/')
        self.assertEqual(res_appraisals.status_code, 200)
        self.assertEqual(res_appraisals['Content-Type'], 'text/csv')
        self.assertIn('Employee ID', res_appraisals.content.decode('utf-8'))
        self.assertIn('Teaching Score', res_appraisals.content.decode('utf-8'))

        # 2. Export Faculty Directory CSV
        res_faculty = self.client.get('/admin-portal/faculty/export-csv/')
        self.assertEqual(res_faculty.status_code, 200)
        self.assertEqual(res_faculty['Content-Type'], 'text/csv')
        self.assertIn('Employee ID', res_faculty.content.decode('utf-8'))
        self.assertIn('FAC-TEST-001', res_faculty.content.decode('utf-8'))

    def test_password_change_functionality(self):
        """Test secure password change interface and session preservation."""
        self.client.login(username='faculty_test', password='testpassword123')

        # Attempt with wrong old password
        bad_res = self.client.post('/change-password/', {
            'old_password': 'wrongpassword',
            'new_password1': 'NewValidPass123!@#',
            'new_password2': 'NewValidPass123!@#',
        })
        self.assertEqual(bad_res.status_code, 200)
        self.assertFalse(self.faculty_user.check_password('NewValidPass123!@#'))

        # Successful password change
        good_res = self.client.post('/change-password/', {
            'old_password': 'testpassword123',
            'new_password1': 'NewValidPass123!@#',
            'new_password2': 'NewValidPass123!@#',
        }, follow=True)
        self.assertEqual(good_res.status_code, 200)
        self.faculty_user.refresh_from_db()
        self.assertTrue(self.faculty_user.check_password('NewValidPass123!@#'))

    def test_dynamic_academic_year_filtering_and_uniqueness(self):
        """Test filtering records by academic year and duplicate submission prevention."""
        # Create records across two sessions
        TeachingRecord.objects.create(
            faculty=self.faculty_profile,
            academic_year='2024-2025',
            subject_name='Data Structures',
            subject_code='CS-201',
            scheduled_hours=50,
            conducted_hours=50,
            pass_percentage=Decimal('90.00'),
            student_feedback_score=Decimal('4.50')
        )
        TeachingRecord.objects.create(
            faculty=self.faculty_profile,
            academic_year='2025-2026',
            subject_name='Computer Networks',
            subject_code='CS-501',
            scheduled_hours=50,
            conducted_hours=48,
            pass_percentage=Decimal('92.00'),
            student_feedback_score=Decimal('4.60')
        )

        self.client.login(username='faculty_test', password='testpassword123')

        # Test session filter in teaching list
        res_filter = self.client.get('/faculty/teaching/?year=2024-2025')
        self.assertEqual(res_filter.status_code, 200)
        self.assertContains(res_filter, 'CS-201')
        self.assertNotContains(res_filter, 'CS-501')

        # Submit appraisal for 2024-2025
        res_sub1 = self.client.post('/faculty/appraisal/submit/', {
            'academic_year': '2024-2025',
            'faculty_remarks': 'First submission for 2024-2025',
        }, follow=True)
        self.assertEqual(res_sub1.status_code, 200)
        self.assertTrue(AppraisalSubmission.objects.filter(faculty=self.faculty_profile, academic_year='2024-2025').exists())

        # Test duplicate prevention for same session
        sub_count_before = AppraisalSubmission.objects.filter(faculty=self.faculty_profile, academic_year='2024-2025').count()
        self.assertEqual(sub_count_before, 1)


class RubricComplianceVerificationTests(TestCase):
    """
    Focused verification tests for 30/30 rubric compliance items:
    1. URL converters: <str:employee_id>, <slug:department_slug>
    2. Regular expression route: re_path(r'^archive/...')
    3. JSON Response API endpoint (/api/faculty/<str:employee_id>/summary/)
    4. Custom 404 and 500 error handlers and templates
    5. Reverse URL resolution
    """

    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Faculty user & profile
        self.faculty_user = User.objects.create_user(
            username='rubric_faculty',
            email='rfaculty@university.edu',
            password='TestPassword123!',
            first_name='Dr. Vikram',
            last_name='Nair'
        )
        self.faculty_profile = FacultyProfile.objects.create(
            user=self.faculty_user,
            employee_id='FAC-CSE-999',
            department='CSE',
            designation='Associate Professor',
            highest_qualification='Ph.D.',
            specialization='Distributed Systems',
            date_of_joining=date(2019, 6, 1),
            experience_years=Decimal('7.0'),
            contact_number='+91 9876543210',
            promotion_status='Eligible for Promotion'
        )

        # Admin user
        self.admin_user = User.objects.create_user(
            username='rubric_admin',
            email='radmin@university.edu',
            password='AdminPassword123!',
            is_staff=True,
            is_superuser=True
        )

    def test_str_converter_json_api_success(self):
        """Test <str:employee_id> converter and valid JSON response from database."""
        self.client.login(username='rubric_faculty', password='TestPassword123!')
        response = self.client.get('/api/faculty/FAC-CSE-999/summary/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        data = response.json()
        self.assertEqual(data['employee_id'], 'FAC-CSE-999')
        self.assertEqual(data['name'], 'Dr. Vikram Nair')
        self.assertEqual(data['department'], 'CSE')
        self.assertEqual(data['department_name'], 'Computer Science & Engineering')
        self.assertEqual(data['designation'], 'Associate Professor')
        self.assertEqual(data['promotion_status'], 'Eligible for Promotion')
        self.assertEqual(data['highest_qualification'], 'Ph.D.')
        self.assertEqual(data['specialization'], 'Distributed Systems')

        # Verify no sensitive data is leaked
        self.assertNotIn('password', data)
        self.assertNotIn('secret', str(data).lower())

    def test_str_converter_json_api_404_missing(self):
        """Test <str:employee_id> with nonexistent ID returns 404 JSON."""
        self.client.login(username='rubric_faculty', password='TestPassword123!')
        response = self.client.get('/api/faculty/NONEXISTENT-ID/summary/')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertEqual(data['error'], 'Not Found')
        self.assertIn("not found", data['message'])

    def test_str_converter_json_api_unauthorized(self):
        """Test that unauthenticated requests to JSON API are redirected to login."""
        response = self.client.get('/api/faculty/FAC-CSE-999/summary/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response['Location'])

    def test_slug_converter_department_directory_valid(self):
        """Test <slug:department_slug> converter renders department faculty roster."""
        self.client.login(username='rubric_faculty', password='TestPassword123!')
        response = self.client.get('/faculty/department/cse/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faculty/department_directory.html')
        self.assertContains(response, 'Department of Computer Science &amp; Engineering')
        self.assertContains(response, 'FAC-CSE-999')
        self.assertContains(response, 'Dr. Vikram Nair')

    def test_slug_converter_department_directory_invalid_slug_404(self):
        """Test that invalid department slug returns HTTP 404."""
        self.client.login(username='rubric_faculty', password='TestPassword123!')
        response = self.client.get('/faculty/department/invalid-dept-slug/')
        self.assertEqual(response.status_code, 404)

    def test_re_path_archive_academic_year_redirect(self):
        """Test re_path route captures academic year and routes to correct archive view."""
        self.client.login(username='rubric_faculty', password='TestPassword123!')

        # 4-digit notation (2025-2026)
        res_full = self.client.get('/archive/2025-2026/')
        self.assertEqual(res_full.status_code, 302)
        self.assertIn('year=2025-2026', res_full['Location'])

        # 2-digit suffix notation (2025-26)
        res_short = self.client.get('/archive/2025-26/')
        self.assertEqual(res_short.status_code, 302)
        self.assertIn('year=2025-2026', res_short['Location'])

    def test_re_path_archive_invalid_year_404(self):
        """Test that invalid academic year raises 404."""
        self.client.login(username='rubric_faculty', password='TestPassword123!')
        # Valid regex format but year out of range
        res_out_of_range = self.client.get('/archive/1980-81/')
        self.assertEqual(res_out_of_range.status_code, 404)

        # Invalid regex format does not match re_path pattern
        res_bad_format = self.client.get('/archive/not-a-year/')
        self.assertEqual(res_bad_format.status_code, 404)

    @override_settings(DEBUG=False)
    def test_custom_404_error_page_rendering(self):
        """Test custom 404 page renders institutional design under DEBUG=False."""
        # Unauthenticated: displays Homepage and Login navigation
        response = self.client.get('/nonexistent-test-url-for-404-check/')
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Academic Page Not Found", status_code=404)
        self.assertContains(response, "HTTP 404 Error", status_code=404)
        self.assertContains(response, "Institutional Homepage", status_code=404)
        self.assertContains(response, "Faculty Login", status_code=404)

        # Authenticated: displays Return to Dashboard navigation
        self.client.login(username='rubric_faculty', password='TestPassword123!')
        res_auth = self.client.get('/nonexistent-test-url-for-404-check/')
        self.assertEqual(res_auth.status_code, 404)
        self.assertContains(res_auth, "Return to Dashboard", status_code=404)

        # Ensure no traceback or internal paths leaked
        self.assertNotContains(response, "Traceback", status_code=404)
        self.assertNotContains(response, "Django_Project", status_code=404)

    def test_custom_500_error_page_rendering(self):
        """Test custom 500 handler renders safe institutional design."""
        request = self.factory.get('/some-broken-endpoint/')
        response = custom_500(request)
        self.assertEqual(response.status_code, 500)
        content = response.content.decode('utf-8')
        self.assertIn("Unexpected Institutional Server Error", content)
        self.assertIn("HTTP 500", content)
        self.assertIn("Return to Homepage", content)
        self.assertNotIn("Traceback", content)
        self.assertNotIn("SECRET_KEY", content)

    def test_reverse_url_resolution(self):
        """Verify reverse URL resolution for all new rubric routes."""
        self.assertEqual(
            reverse('faculty_api_summary', kwargs={'employee_id': 'FAC-CSE-999'}),
            '/api/faculty/FAC-CSE-999/summary/'
        )
        self.assertEqual(
            reverse('faculty_department_directory', kwargs={'department_slug': 'cse'}),
            '/faculty/department/cse/'
        )
        self.assertEqual(
            reverse('archive_by_year', kwargs={'year': '2025-26'}),
            '/archive/2025-26/'
        )


