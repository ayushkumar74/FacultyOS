"""
FacultyOS — Realistic Institutional Demo Data Seeder
====================================================
IMPORTANT NOTICE / DEMO DATA DISCLAIMER:
This script populates the database with realistic, entirely synthetic sample
faculty portfolios, teaching records, research citations, and appraisals designed
strictly for evaluation, grading, and demonstration purposes.

- No data belongs to an actual university, living individual, or commercial entity.
- Seeded credentials (e.g. admin/admin123, rsharma/faculty123) are demo-only.
- All records use standardized UGC/AICTE-aligned academic formats.
"""

import os
import django
from decimal import Decimal
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'faculty_portal.settings')
django.setup()

from django.contrib.auth.models import User
from appraisal.models import (
    FacultyProfile,
    TeachingRecord,
    ResearchPublication,
    WorkshopTraining,
    CompletedProject,
    AppraisalSubmission,
)
from appraisal.scoring import calculate_appraisal_score

def run_seed():
    print("==================================================================")
    print("FacultyOS: Seeding Database with Realistic Synthetic Sample Data")
    print("DISCLAIMER: All seeded accounts and records are synthetic demo data")
    print("==================================================================")

    # 1. Create Superuser (Admin)
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@university.edu',
            'first_name': 'Dean Academic',
            'last_name': 'Office',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    print("Admin user created: admin / admin123")

    # 2. Create Faculty 1: Dr. Rajesh Sharma (CSE)
    f1_user, _ = User.objects.get_or_create(
        username='rsharma',
        defaults={
            'email': 'r.sharma@university.edu',
            'first_name': 'Dr. Rajesh',
            'last_name': 'Sharma',
        }
    )
    f1_user.set_password('faculty123')
    f1_user.save()

    f1_profile, _ = FacultyProfile.objects.get_or_create(
        user=f1_user,
        defaults={
            'employee_id': 'FAC-CSE-001',
            'department': 'CSE',
            'designation': 'Associate Professor',
            'highest_qualification': 'Ph.D.',
            'specialization': 'Cloud Computing & Artificial Intelligence',
            'date_of_joining': date(2018, 7, 15),
            'experience_years': Decimal('8.5'),
            'contact_number': '+91 9876543210',
            'address': 'Staff Quarters B-12, University Campus',
            'promotion_status': 'Eligible for Promotion',
            'promotion_eligible_date': date(2026, 1, 10),
        }
    )

    # Teaching Records for Faculty 1
    TeachingRecord.objects.get_or_create(
        faculty=f1_profile,
        academic_year='2025-2026',
        subject_code='CS-501',
        defaults={
            'subject_name': 'Distributed Systems & Cloud Computing',
            'semester': 'Odd',
            'course_type': 'Theory',
            'scheduled_hours': 54,
            'conducted_hours': 52,
            'pass_percentage': Decimal('94.80'),
            'student_feedback_score': Decimal('4.65'),
            'innovative_teaching_methods': 'Flipped classroom, Docker containerization hands-on labs.',
        }
    )

    TeachingRecord.objects.get_or_create(
        faculty=f1_profile,
        academic_year='2025-2026',
        subject_code='CS-505',
        defaults={
            'subject_name': 'Cloud Computing Laboratory',
            'semester': 'Odd',
            'course_type': 'Practical',
            'scheduled_hours': 36,
            'conducted_hours': 36,
            'pass_percentage': Decimal('98.00'),
            'student_feedback_score': Decimal('4.80'),
            'innovative_teaching_methods': 'AWS Educate & Google Cloud real cluster deployments.',
        }
    )

    TeachingRecord.objects.get_or_create(
        faculty=f1_profile,
        academic_year='2025-2026',
        subject_code='CS-602',
        defaults={
            'subject_name': 'Big Data Analytics',
            'semester': 'Even',
            'course_type': 'Theory',
            'scheduled_hours': 50,
            'conducted_hours': 49,
            'pass_percentage': Decimal('91.50'),
            'student_feedback_score': Decimal('4.55'),
            'innovative_teaching_methods': 'Apache Spark case studies and Kaggle datasets.',
        }
    )

    # Research Publications for Faculty 1
    ResearchPublication.objects.get_or_create(
        faculty=f1_profile,
        title='Adaptive Resource Scheduling in Edge-Cloud Computing Environments',
        defaults={
            'academic_year': '2025-2026',
            'journal_conference_name': 'IEEE Transactions on Services Computing',
            'publication_type': 'SCI_SCOPUS',
            'issn_isbn': 'ISSN 1939-1374',
            'publication_date': date(2025, 9, 20),
            'indexing_details': 'SCI Impact Factor 5.8, Scopus Q1',
            'author_role': 'First Author',
            'doi_or_url': 'https://doi.org/10.1109/TSC.2025.321045',
        }
    )

    ResearchPublication.objects.get_or_create(
        faculty=f1_profile,
        title='Deep Learning Framework for Real-time Anomaly Detection in Microservices',
        defaults={
            'academic_year': '2025-2026',
            'journal_conference_name': 'International Conference on Software Engineering (ICSE 2025)',
            'publication_type': 'INT_CONF',
            'issn_isbn': 'ISBN 978-1-4503-9000-0',
            'publication_date': date(2025, 11, 5),
            'indexing_details': 'IEEE / ACM Proceedings Core A',
            'author_role': 'First Author',
            'doi_or_url': 'https://doi.org/10.1145/3345.2025',
        }
    )

    ResearchPublication.objects.get_or_create(
        faculty=f1_profile,
        title='A System and Method for Automated Fault Tolerant Microservice Provisioning',
        defaults={
            'academic_year': '2025-2026',
            'journal_conference_name': 'Indian Patent Office',
            'publication_type': 'PATENT',
            'issn_isbn': 'Patent App 202511098421',
            'publication_date': date(2026, 1, 15),
            'indexing_details': 'Published Official Gazette',
            'author_role': 'First Author',
            'doi_or_url': 'https://ipindia.gov.in/patents',
        }
    )

    # Workshops for Faculty 1
    WorkshopTraining.objects.get_or_create(
        faculty=f1_profile,
        title='AICTE ATAL Faculty Development Program on Generative AI & High Performance Computing',
        defaults={
            'academic_year': '2025-2026',
            'program_type': 'FDP',
            'role': 'Participant',
            'organizing_institution': 'IIT Roorkee & AICTE',
            'start_date': date(2025, 10, 10),
            'end_date': date(2025, 10, 15),
            'duration_days': 6,
            'certificate_link': 'https://storage.university.edu/certificates/atal_rsharma.pdf',
        }
    )

    WorkshopTraining.objects.get_or_create(
        faculty=f1_profile,
        title='International Workshop on Sustainable Cloud Architecture and Microservices',
        defaults={
            'academic_year': '2025-2026',
            'program_type': 'WORKSHOP',
            'role': 'Resource Person',
            'organizing_institution': 'NIT Karnataka, Surathkal',
            'start_date': date(2025, 12, 1),
            'end_date': date(2025, 12, 3),
            'duration_days': 3,
            'certificate_link': 'https://storage.university.edu/certificates/nitk_keynote.pdf',
        }
    )

    # Completed Projects for Faculty 1
    CompletedProject.objects.get_or_create(
        faculty=f1_profile,
        title='Scalable IoT-Edge Middleware for Smart Agriculture Monitoring in Rural India',
        defaults={
            'academic_year': '2025-2026',
            'funding_agency': 'Department of Science & Technology (DST-SERB)',
            'project_type': 'RESEARCH_GRANT',
            'grant_amount': Decimal('1850000.00'),
            'duration_months': 24,
            'role': 'PI',
            'status': 'Completed',
            'completion_date': date(2025, 11, 30),
            'outcomes_summary': 'Developed low-cost IoT sensor gateway, filed 1 patent, published 2 Scopus papers.',
        }
    )

    # Calculate and create submission for Faculty 1
    score1 = calculate_appraisal_score(f1_profile, '2025-2026')
    AppraisalSubmission.objects.get_or_create(
        faculty=f1_profile,
        academic_year='2025-2026',
        defaults={
            'status': 'APPROVED',
            'teaching_score': score1['teaching_score'],
            'research_score': score1['research_score'],
            'workshop_score': score1['workshop_score'],
            'project_score': score1['project_score'],
            'total_score': score1['total_score'],
            'performance_grade': score1['performance_grade'],
            'faculty_remarks': 'Successfully achieved all instructional outcomes with high student satisfaction (4.65/5). Filed 1 patent and secured DST grant completion. Eager to advance to Professor rank under CAS.',
            'admin_remarks': 'Exemplary teaching dedication, strong high-impact research output (IEEE Trans.), and completed sponsored research grant. Recommended for Promotion to Professor.',
            'promotion_recommendation': 'Recommended for Promotion',
            'reviewed_by': admin_user,
            'reviewed_at': django.utils.timezone.now(),
        }
    )

    # 3. Create Faculty 2: Dr. Priya Nair (ECE)
    f2_user, _ = User.objects.get_or_create(
        username='pnair',
        defaults={
            'email': 'p.nair@university.edu',
            'first_name': 'Dr. Priya',
            'last_name': 'Nair',
        }
    )
    f2_user.set_password('faculty123')
    f2_user.save()

    f2_profile, _ = FacultyProfile.objects.get_or_create(
        user=f2_user,
        defaults={
            'employee_id': 'FAC-ECE-002',
            'department': 'ECE',
            'designation': 'Assistant Professor',
            'highest_qualification': 'Ph.D.',
            'specialization': 'VLSI Signal Processing & Embedded Systems',
            'date_of_joining': date(2021, 8, 1),
            'experience_years': Decimal('4.5'),
            'contact_number': '+91 9811223344',
            'promotion_status': 'Under Review',
        }
    )

    TeachingRecord.objects.get_or_create(
        faculty=f2_profile,
        academic_year='2025-2026',
        subject_code='EC-401',
        defaults={
            'subject_name': 'Digital Signal Processing',
            'semester': 'Odd',
            'course_type': 'Theory',
            'scheduled_hours': 48,
            'conducted_hours': 47,
            'pass_percentage': Decimal('92.00'),
            'student_feedback_score': Decimal('4.40'),
            'innovative_teaching_methods': 'MATLAB simulation demonstrations and DSP board prototyping.',
        }
    )

    ResearchPublication.objects.get_or_create(
        faculty=f2_profile,
        title='Energy Efficient Low-Power Approximate Adders for Biomedical Signal Processors',
        defaults={
            'academic_year': '2025-2026',
            'journal_conference_name': 'Microprocessors and Microsystems (Elsevier)',
            'publication_type': 'SCI_SCOPUS',
            'issn_isbn': 'ISSN 0141-9331',
            'publication_date': date(2025, 8, 14),
            'indexing_details': 'Scopus Q2, IF 2.8',
            'author_role': 'First Author',
        }
    )

    WorkshopTraining.objects.get_or_create(
        faculty=f2_profile,
        title='One-Week Workshop on Cadence EDA Tools for Advanced VLSI Design',
        defaults={
            'academic_year': '2025-2026',
            'program_type': 'WORKSHOP',
            'role': 'Participant',
            'organizing_institution': 'IIT Madras',
            'start_date': date(2025, 9, 12),
            'end_date': date(2025, 9, 17),
            'duration_days': 6,
        }
    )

    score2 = calculate_appraisal_score(f2_profile, '2025-2026')
    AppraisalSubmission.objects.get_or_create(
        faculty=f2_profile,
        academic_year='2025-2026',
        defaults={
            'status': 'SUBMITTED',
            'teaching_score': score2['teaching_score'],
            'research_score': score2['research_score'],
            'workshop_score': score2['workshop_score'],
            'project_score': score2['project_score'],
            'total_score': score2['total_score'],
            'performance_grade': score2['performance_grade'],
            'faculty_remarks': 'Mentored 2 final year undergraduate projects and delivered curriculum as per lesson plan. Completed 1 Elsevier paper.',
            'promotion_recommendation': 'Deferred / Under Review',
        }
    )

    # 4. Create Faculty 3: Dr. Amit Patel (Mechanical)
    f3_user, _ = User.objects.get_or_create(
        username='apatel',
        defaults={
            'email': 'a.patel@university.edu',
            'first_name': 'Dr. Amit',
            'last_name': 'Patel',
        }
    )
    f3_user.set_password('faculty123')
    f3_user.save()

    f3_profile, _ = FacultyProfile.objects.get_or_create(
        user=f3_user,
        defaults={
            'employee_id': 'FAC-MECH-003',
            'department': 'MECH',
            'designation': 'Professor',
            'highest_qualification': 'Ph.D.',
            'specialization': 'Thermal Engineering & Renewable Energy Systems',
            'date_of_joining': date(2012, 1, 10),
            'experience_years': Decimal('14.0'),
            'contact_number': '+91 9723456789',
            'promotion_status': 'Promoted',
        }
    )

    TeachingRecord.objects.get_or_create(
        faculty=f3_profile,
        academic_year='2025-2026',
        subject_code='ME-701',
        defaults={
            'subject_name': 'Renewable Energy Systems & Solar Thermodynamics',
            'semester': 'Odd',
            'course_type': 'Theory',
            'scheduled_hours': 52,
            'conducted_hours': 52,
            'pass_percentage': Decimal('96.00'),
            'student_feedback_score': Decimal('4.70'),
        }
    )

    CompletedProject.objects.get_or_create(
        faculty=f3_profile,
        title='Industrial Consultancy: Thermal Performance Optimization for Heavy Heat Exchangers',
        defaults={
            'academic_year': '2025-2026',
            'funding_agency': 'Bharat Heavy Electricals Limited (BHEL)',
            'project_type': 'CONSULTANCY',
            'grant_amount': Decimal('620000.00'),
            'duration_months': 12,
            'role': 'LEAD',
            'status': 'Completed',
        }
    )

    score3 = calculate_appraisal_score(f3_profile, '2025-2026')
    AppraisalSubmission.objects.get_or_create(
        faculty=f3_profile,
        academic_year='2025-2026',
        defaults={
            'status': 'APPROVED',
            'teaching_score': score3['teaching_score'],
            'research_score': score3['research_score'],
            'workshop_score': score3['workshop_score'],
            'project_score': score3['project_score'],
            'total_score': score3['total_score'],
            'performance_grade': score3['performance_grade'],
            'faculty_remarks': 'Conducted BHEL industrial consultancy and trained M.Tech scholars.',
            'admin_remarks': 'Outstanding industrial engagement and leadership. Promoted.',
            'promotion_recommendation': 'Eligible - Promotion Awarded',
            'reviewed_by': admin_user,
            'reviewed_at': django.utils.timezone.now(),
        }
    )

    # 5. Create Faculty 4: Dr. Sunita Rao (IT)
    f4_user, _ = User.objects.get_or_create(
        username='srao',
        defaults={
            'email': 's.rao@university.edu',
            'first_name': 'Dr. Sunita',
            'last_name': 'Rao',
        }
    )
    f4_user.set_password('faculty123')
    f4_user.save()

    FacultyProfile.objects.get_or_create(
        user=f4_user,
        defaults={
            'employee_id': 'FAC-IT-004',
            'department': 'IT',
            'designation': 'Assistant Professor',
            'highest_qualification': 'Ph.D.',
            'specialization': 'Information Security & Blockchain Technology',
            'date_of_joining': date(2022, 6, 1),
            'experience_years': Decimal('3.5'),
            'contact_number': '+91 9988776655',
            'promotion_status': 'Not Applied',
        }
    )

    print("--- Database Seeding Completed Successfully! ---")

if __name__ == '__main__':
    run_seed()

