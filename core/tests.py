from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from datetime import date
from appraisal.models import (
    FacultyProfile,
    TeachingRecord,
    ResearchPublication,
    WorkshopTraining,
    CompletedProject,
    AppraisalSubmission,
)
from appraisal.scoring import calculate_appraisal_score


class AuthenticationAndRoleWorkflowTests(TestCase):
    """
    Exhaustive test suite covering realistic authentication, role isolation,
    duplicate account prevention, administrative onboarding, and end-to-end appraisal workflow.
    """

    def setUp(self):
        self.client = Client()

        # 1. Seed Admin User
        self.admin = User.objects.create_user(
            username='dean_academic',
            email='dean@university.edu',
            password='AdminPassword123!',
            first_name='Prof. Vikram',
            last_name='Mehta',
            is_staff=True,
            is_superuser=True
        )

        # 2. Seed Faculty User & Profile
        self.faculty_user = User.objects.create_user(
            username='rsharma',
            email='rsharma@university.edu',
            password='FacultyPassword123!',
            first_name='Dr. Rajesh',
            last_name='Sharma'
        )
        self.faculty_profile = FacultyProfile.objects.create(
            user=self.faculty_user,
            employee_id='FAC-CSE-001',
            department='CSE',
            designation='Associate Professor',
            highest_qualification='Ph.D.',
            specialization='Cloud Computing',
            date_of_joining=date(2018, 7, 15),
            experience_years=Decimal('8.5'),
            contact_number='+91 9876543210',
            promotion_status='Under Review'
        )

    def test_login_with_username_and_employee_id(self):
        """Test that faculty can log in using either username or official Employee ID."""
        # 1. Login with username
        res_user = self.client.post('/login/', {
            'username': 'rsharma',
            'password': 'FacultyPassword123!',
        }, follow=True)
        self.assertEqual(res_user.status_code, 200)
        self.assertTrue(res_user.context['user'].is_authenticated)
        self.assertEqual(res_user.context['user'].username, 'rsharma')
        self.client.logout()

        # 2. Login with Employee ID (case-insensitive)
        res_emp = self.client.post('/login/', {
            'username': 'fac-cse-001',
            'password': 'FacultyPassword123!',
        }, follow=True)
        self.assertEqual(res_emp.status_code, 200)
        self.assertTrue(res_emp.context['user'].is_authenticated)
        self.assertEqual(res_emp.context['user'].username, 'rsharma')
        self.client.logout()

        # 3. Invalid credentials rejected
        res_bad = self.client.post('/login/', {
            'username': 'rsharma',
            'password': 'WrongPassword!',
        })
        self.assertEqual(res_bad.status_code, 200)
        self.assertContains(res_bad, "Invalid username/Employee ID or password")

    def test_faculty_registration_and_admin_prevention(self):
        """
        Test public faculty registration:
        - Prevents registering with reserved admin usernames.
        - Guarantees registered user has is_staff=False and is_superuser=False.
        - Prevents duplicate usernames, emails, and Employee IDs.
        """
        # 1. Attempt registering with reserved username 'admin'
        res_admin_reg = self.client.post('/register/', {
            'first_name': 'Attacker',
            'last_name': 'Admin',
            'username': 'admin',
            'email': 'attacker@test.edu',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
            'employee_id': 'FAC-ATK-999',
            'department': 'CSE',
            'designation': 'Assistant Professor',
            'highest_qualification': 'Ph.D.',
            'specialization': 'Security',
            'date_of_joining': '2023-01-01',
            'experience_years': '2.0',
            'contact_number': '+91 9999900000',
        })
        self.assertEqual(res_admin_reg.status_code, 200)
        self.assertContains(res_admin_reg, "reserved for system administration")
        self.assertFalse(User.objects.filter(username='admin', email='attacker@test.edu').exists())

        # 2. Legitimate registration
        res_valid = self.client.post('/register/', {
            'first_name': 'Pooja',
            'last_name': 'Kulkarni',
            'username': 'pkulkarni',
            'email': 'p.kulkarni@university.edu',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
            'employee_id': 'FAC-ECE-010',
            'department': 'ECE',
            'designation': 'Assistant Professor',
            'highest_qualification': 'Ph.D.',
            'specialization': 'Embedded Systems',
            'date_of_joining': '2022-08-01',
            'experience_years': '3.0',
            'contact_number': '+91 9811122233',
        }, follow=True)
        self.assertEqual(res_valid.status_code, 200)
        new_user = User.objects.get(username='pkulkarni')
        self.assertFalse(new_user.is_staff, "Registered user must NOT have staff status")
        self.assertFalse(new_user.is_superuser, "Registered user must NOT have superuser status")
        self.assertTrue(hasattr(new_user, 'faculty_profile'))
        self.assertEqual(new_user.faculty_profile.employee_id, 'FAC-ECE-010')

        # 3. Duplicate checks
        res_dup_user = self.client.post('/register/', {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'pkulkarni',  # Duplicate
            'email': 'different@university.edu',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
            'employee_id': 'FAC-NEW-099',
            'department': 'IT',
            'designation': 'Assistant Professor',
            'highest_qualification': 'Ph.D.',
        })
        self.assertEqual(res_dup_user.status_code, 200)
        self.assertContains(res_dup_user, "already taken")

        res_dup_empid = self.client.post('/register/', {
            'first_name': 'Test',
            'last_name': 'User',
            'username': 'unique_user',
            'email': 'unique@university.edu',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
            'employee_id': 'FAC-ECE-010',  # Duplicate employee ID
            'department': 'IT',
            'designation': 'Assistant Professor',
            'highest_qualification': 'Ph.D.',
        })
        self.assertEqual(res_dup_empid.status_code, 200)
        self.assertContains(res_dup_empid, "Employee ID is already registered")

    def test_role_based_access_isolation(self):
        """Test access control: Anonymous, Faculty, and Admin role isolation."""
        # Anonymous users blocked from protected areas
        self.assertEqual(self.client.get('/faculty/dashboard/').status_code, 302)
        self.assertEqual(self.client.get('/admin-portal/dashboard/').status_code, 302)

        # Faculty user logged in
        self.client.login(username='rsharma', password='FacultyPassword123!')
        # Can access faculty dashboard
        self.assertEqual(self.client.get('/faculty/dashboard/').status_code, 200)
        # Blocked from admin portal (redirected with warning)
        res_faculty_admin = self.client.get('/admin-portal/dashboard/')
        self.assertEqual(res_faculty_admin.status_code, 302)
        self.client.logout()

        # Admin user logged in
        self.client.login(username='dean_academic', password='AdminPassword123!')
        # Can access admin portal
        self.assertEqual(self.client.get('/admin-portal/dashboard/').status_code, 200)
        self.assertEqual(self.client.get('/admin-portal/faculty/').status_code, 200)
        self.client.logout()

    def test_admin_onboards_faculty_member(self):
        """Test administrative onboarding view (/admin-portal/faculty/add/)."""
        self.client.login(username='dean_academic', password='AdminPassword123!')

        # 1. Admin navigates to add faculty form
        res_get = self.client.get('/admin-portal/faculty/add/')
        self.assertEqual(res_get.status_code, 200)
        self.assertContains(res_get, "Onboard New Faculty Member")

        # 2. Admin submits new faculty profile
        res_post = self.client.post('/admin-portal/faculty/add/', {
            'first_name': 'Dr. Sunita',
            'last_name': 'Raman',
            'username': 'sraman',
            'email': 's.raman@university.edu',
            'temporary_password': 'TempPassword123!',
            'employee_id': 'FAC-MECH-008',
            'department': 'MECH',
            'designation': 'Assistant Professor',
            'highest_qualification': 'Ph.D.',
            'specialization': 'Robotics & Automation',
            'date_of_joining': '2024-01-15',
            'experience_years': '4.0',
            'contact_number': '+91 9822334455',
            'promotion_status': 'Not Applied',
            'address': 'Campus Quarters C-4',
        }, follow=True)

        self.assertEqual(res_post.status_code, 200)
        self.assertTrue(User.objects.filter(username='sraman').exists())
        new_faculty = User.objects.get(username='sraman')
        self.assertFalse(new_faculty.is_staff)
        self.assertEqual(new_faculty.faculty_profile.employee_id, 'FAC-MECH-008')

        # 3. New faculty logs in with credentials
        self.client.logout()
        res_login = self.client.post('/login/', {
            'username': 'sraman',
            'password': 'TempPassword123!',
        }, follow=True)
        self.assertEqual(res_login.status_code, 200)
        self.assertEqual(res_login.context['user'].username, 'sraman')

    def test_complete_real_world_appraisal_workflow(self):
        """
        Verify the complete 9-stage institutional university workflow:
        1. Admin creates faculty account.
        2. Faculty logs in.
        3. Faculty creates Category I-IV records.
        4. Faculty submits annual self-appraisal.
        5. Automated PBAS score calculation.
        6. Admin reviews appraisal queue.
        7. Admin evaluates, awards committee marks, and approves.
        8. CAS promotion recommendation and status updated.
        9. Faculty views final approved appraisal & downloads certified PDF.
        """
        # Step 1: Admin creates faculty
        self.client.login(username='dean_academic', password='AdminPassword123!')
        res_create = self.client.post('/admin-portal/faculty/add/', {
            'first_name': 'Kavita',
            'last_name': 'Nambiar',
            'username': 'knambiar',
            'email': 'k.nambiar@university.edu',
            'temporary_password': 'FacultyPass123!',
            'employee_id': 'FAC-IT-025',
            'department': 'IT',
            'designation': 'Assistant Professor',
            'highest_qualification': 'Ph.D.',
            'specialization': 'Cybersecurity & Cryptography',
            'date_of_joining': '2021-08-01',
            'experience_years': '5.0',
            'contact_number': '+91 9711223344',
            'promotion_status': 'Under Review',
        }, follow=True)
        self.assertEqual(res_create.status_code, 200)
        self.client.logout()

        # Step 2: Faculty logs in
        login_res = self.client.post('/login/', {
            'username': 'FAC-IT-025',  # Using Employee ID
            'password': 'FacultyPass123!',
        }, follow=True)
        self.assertEqual(login_res.status_code, 200)
        faculty_user = User.objects.get(username='knambiar')
        faculty_profile = faculty_user.faculty_profile

        # Step 3: Faculty adds records for 2025-2026
        # A. Teaching Record (Cat I)
        res_t = self.client.post('/faculty/teaching/add/', {
            'academic_year': '2025-2026',
            'semester': 'Odd',
            'subject_name': 'Network Security',
            'subject_code': 'IT-401',
            'course_type': 'Theory',
            'scheduled_hours': 54,
            'conducted_hours': 54,
            'pass_percentage': '96.00',
            'student_feedback_score': '4.80',
            'innovative_teaching_methods': 'Capture The Flag labs',
        }, follow=True)
        self.assertEqual(res_t.status_code, 200)

        # B. Research Publication (Cat II)
        res_r = self.client.post('/faculty/research/add/', {
            'academic_year': '2025-2026',
            'title': 'Zero Knowledge Proofs in Blockchain',
            'journal_conference_name': 'IEEE Transactions on Dependable and Secure Computing',
            'publication_type': 'SCI_SCOPUS',
            'issn_isbn': 'ISSN 1545-5971',
            'publication_date': '2025-10-15',
            'indexing_details': 'SCI Impact Factor 7.3, Scopus Q1',
            'author_role': 'First Author',
            'doi_or_url': 'https://doi.org/10.1109/TDSC.2025.1001',
        }, follow=True)
        self.assertEqual(res_r.status_code, 200)

        # C. Workshop / FDP (Cat III)
        res_w = self.client.post('/faculty/workshops/add/', {
            'academic_year': '2025-2026',
            'title': 'AICTE ATAL FDP on Quantum Cryptography',
            'program_type': 'FDP',
            'role': 'Participant',
            'organizing_institution': 'IIT Madras',
            'start_date': '2025-11-10',
            'end_date': '2025-11-15',
            'duration_days': 6,
        }, follow=True)
        self.assertEqual(res_w.status_code, 200)

        # D. Sponsored Project (Cat IV)
        res_p = self.client.post('/faculty/projects/add/', {
            'academic_year': '2025-2026',
            'title': 'Next-Gen Cryptographic Protocol Testing',
            'funding_agency': 'DST-SERB',
            'project_type': 'RESEARCH_GRANT',
            'grant_amount': '1200000.00',
            'duration_months': 18,
            'role': 'PI',
            'status': 'Completed',
        }, follow=True)
        self.assertEqual(res_p.status_code, 200)

        # Step 4 & 5: Faculty submits annual self-appraisal (PBAS calculated)
        res_sub = self.client.post('/faculty/appraisal/submit/', {
            'academic_year': '2025-2026',
            'faculty_remarks': 'Delivered high academic results and completed DST funded research.',
        }, follow=True)
        self.assertEqual(res_sub.status_code, 200)

        submission = AppraisalSubmission.objects.get(faculty=faculty_profile, academic_year='2025-2026')
        self.assertEqual(submission.status, 'SUBMITTED')
        # Check PBAS scoring
        self.assertGreater(submission.teaching_score, Decimal('35.00'))
        self.assertEqual(submission.research_score, Decimal('10.00'))
        self.assertEqual(submission.workshop_score, Decimal('5.00'))
        self.assertEqual(submission.project_score, Decimal('10.00'))
        self.assertGreater(submission.total_score, Decimal('60.00'))
        self.client.logout()

        # Step 6, 7 & 8: Admin reviews appraisal in queue, approves and awards CAS promotion
        self.client.login(username='dean_academic', password='AdminPassword123!')
        res_review_page = self.client.get(f'/admin-portal/appraisals/{submission.pk}/review/')
        self.assertEqual(res_review_page.status_code, 200)
        self.assertContains(res_review_page, "Delivered high academic results and completed DST funded research.")

        # Also verify research publication is listed in faculty 360 dossier
        res_dossier_admin = self.client.get(f'/admin-portal/faculty/{faculty_profile.pk}/')
        self.assertEqual(res_dossier_admin.status_code, 200)
        self.assertContains(res_dossier_admin, "Zero Knowledge Proofs in Blockchain")

        res_approve = self.client.post(f'/admin-portal/appraisals/{submission.pk}/review/', {
            'status': 'APPROVED',
            'promotion_recommendation': 'Recommended for Promotion',
            'promotion_status': 'Eligible for Promotion',
            'admin_remarks': 'Exemplary teaching, Scopus Q1 publication and sponsored grant. Unanimously recommended for CAS advancement to Associate Professor.',
        }, follow=True)
        self.assertEqual(res_approve.status_code, 200)

        submission.refresh_from_db()
        faculty_profile.refresh_from_db()
        self.assertEqual(submission.status, 'APPROVED')
        self.assertEqual(submission.reviewed_by, self.admin)
        self.assertIsNotNone(submission.reviewed_at)
        self.assertEqual(faculty_profile.promotion_status, 'Eligible for Promotion')
        self.client.logout()

        # Step 9: Faculty logs in, checks status, downloads certified PDF
        self.client.login(username='knambiar', password='FacultyPass123!')
        res_dossier = self.client.get(f'/faculty/appraisal/{submission.pk}/')
        self.assertEqual(res_dossier.status_code, 200)
        self.assertContains(res_dossier, "Approved")
        self.assertContains(res_dossier, "Recommended for Promotion")

        res_pdf = self.client.get(f'/faculty/appraisal/{submission.pk}/pdf/')
        self.assertEqual(res_pdf.status_code, 200)
        self.assertEqual(res_pdf['Content-Type'], 'application/pdf')
        self.assertTrue(res_pdf.content.startswith(b'%PDF'))
        self.assertGreater(len(res_pdf.content), 2000)
