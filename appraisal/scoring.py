from decimal import Decimal
from .models import (
    TeachingRecord,
    ResearchPublication,
    WorkshopTraining,
    CompletedProject,
)


def calculate_appraisal_score(faculty_profile, academic_year):
    """
    Automated performance evaluation scoring engine.
    Max Total Score: 100 points
      - Teaching Performance: Max 40.0 points
      - Research & Publications: Max 30.0 points
      - Workshops & Training: Max 15.0 points
      - Sponsored Projects & Consultancy: Max 15.0 points
    """
    
    # ----------------------------------------------------
    # 1. TEACHING PERFORMANCE (Max 40.0)
    # ----------------------------------------------------
    teaching_records = TeachingRecord.objects.filter(
        faculty=faculty_profile,
        academic_year=academic_year
    )
    
    teaching_score = Decimal('0.00')
    teaching_breakdown = {
        'count': teaching_records.count(),
        'compliance_pts': Decimal('0.00'),
        'pass_pts': Decimal('0.00'),
        'feedback_pts': Decimal('0.00'),
    }
    
    if teaching_records.exists():
        total_scheduled = sum(t.scheduled_hours for t in teaching_records)
        total_conducted = sum(t.conducted_hours for t in teaching_records)
        avg_pass = sum(t.pass_percentage for t in teaching_records) / Decimal(str(len(teaching_records)))
        avg_feedback = sum(t.student_feedback_score for t in teaching_records) / Decimal(str(len(teaching_records)))
        
        # A. Lecture delivery compliance (Max 20 pts)
        if total_scheduled > 0:
            compliance_ratio = min(Decimal('1.00'), Decimal(str(total_conducted)) / Decimal(str(total_scheduled)))
            compliance_pts = compliance_ratio * Decimal('20.00')
        else:
            compliance_pts = Decimal('0.00')
            
        # B. Average Pass % (Max 10 pts) -> 100% = 10 pts
        pass_pts = (avg_pass / Decimal('100.00')) * Decimal('10.00')
        
        # C. Student Feedback rating (Max 10 pts) -> 5.0 rating = 10 pts
        feedback_pts = (avg_feedback / Decimal('5.00')) * Decimal('10.00')
        
        calculated_teaching = compliance_pts + pass_pts + feedback_pts
        teaching_score = min(Decimal('40.00'), calculated_teaching)
        teaching_breakdown['compliance_pts'] = round(compliance_pts, 2)
        teaching_breakdown['pass_pts'] = round(pass_pts, 2)
        teaching_breakdown['feedback_pts'] = round(feedback_pts, 2)

    # ----------------------------------------------------
    # 2. RESEARCH & PUBLICATIONS (Max 30.0)
    # ----------------------------------------------------
    pub_records = ResearchPublication.objects.filter(
        faculty=faculty_profile,
        academic_year=academic_year
    )
    
    pub_score_accum = Decimal('0.00')
    pub_rates = {
        'SCI_SCOPUS': Decimal('10.00'),
        'PATENT': Decimal('10.00'),
        'UGC_CARE': Decimal('7.00'),
        'INT_CONF': Decimal('5.00'),
        'BOOK_CHAPTER': Decimal('4.00'),
        'NAT_CONF': Decimal('3.00'),
    }
    
    for pub in pub_records:
        base = pub_rates.get(pub.publication_type, Decimal('4.00'))
        # Author weight
        if pub.author_role in ['First Author', 'Corresponding Author']:
            weight = Decimal('1.00')
        else:
            weight = Decimal('0.70')
        pub_score_accum += (base * weight)
        
    research_score = min(Decimal('30.00'), pub_score_accum)

    # ----------------------------------------------------
    # 3. WORKSHOPS & TRAINING (Max 15.0)
    # ----------------------------------------------------
    workshops = WorkshopTraining.objects.filter(
        faculty=faculty_profile,
        academic_year=academic_year
    )
    
    workshop_score_accum = Decimal('0.00')
    workshop_rates = {
        'FDP': Decimal('5.00'),
        'STTP': Decimal('5.00'),
        'ORIENTATION': Decimal('5.00'),
        'WORKSHOP': Decimal('3.00'),
        'SEMINAR': Decimal('2.00'),
    }
    
    for w in workshops:
        base = workshop_rates.get(w.program_type, Decimal('3.00'))
        if w.role in ['Resource Person', 'Coordinator']:
            base += Decimal('2.00')
        workshop_score_accum += base
        
    workshop_score = min(Decimal('15.00'), workshop_score_accum)

    # ----------------------------------------------------
    # 4. SPONSORED PROJECTS & CONSULTANCY (Max 15.0)
    # ----------------------------------------------------
    projects = CompletedProject.objects.filter(
        faculty=faculty_profile,
        academic_year=academic_year
    )
    
    project_score_accum = Decimal('0.00')
    project_rates = {
        'RESEARCH_GRANT': Decimal('10.00'),
        'CONSULTANCY': Decimal('8.00'),
        'INSTITUTIONAL': Decimal('5.00'),
        'STUDENT_MENTOR': Decimal('3.00'),
    }
    
    for proj in projects:
        base = project_rates.get(proj.project_type, Decimal('5.00'))
        if proj.role == 'CO_PI':
            base = base * Decimal('0.70')
        project_score_accum += base
        
    project_score = min(Decimal('15.00'), project_score_accum)

    # ----------------------------------------------------
    # TOTAL & GRADE ASSIGNMENT
    # ----------------------------------------------------
    total_score = min(
        Decimal('100.00'),
        teaching_score + research_score + workshop_score + project_score
    )
    
    # Grading rubric
    if total_score >= Decimal('85.00'):
        grade = "Outstanding (Grade A+)"
        rec = "Recommended for Promotion"
    elif total_score >= Decimal('70.00'):
        grade = "Very Good (Grade A)"
        rec = "Recommended for Promotion"
    elif total_score >= Decimal('55.00'):
        grade = "Good (Grade B)"
        rec = "Deferred / Under Review"
    elif total_score >= Decimal('40.00'):
        grade = "Satisfactory (Grade C)"
        rec = "Deferred / Under Review"
    else:
        grade = "Needs Improvement (Grade D)"
        rec = "Not Recommended"

    return {
        'teaching_score': round(teaching_score, 2),
        'research_score': round(research_score, 2),
        'workshop_score': round(workshop_score, 2),
        'project_score': round(project_score, 2),
        'total_score': round(total_score, 2),
        'performance_grade': grade,
        'promotion_recommendation': rec,
        'teaching_breakdown': teaching_breakdown,
        'counts': {
            'teaching': teaching_records.count(),
            'research': pub_records.count(),
            'workshops': workshops.count(),
            'projects': projects.count(),
        }
    }

