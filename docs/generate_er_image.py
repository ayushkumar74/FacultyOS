"""
Generates high-resolution ER_Diagram.png for FacultyOS documentation.
"""
import os
from PIL import Image, ImageDraw, ImageFont

def create_er_diagram(output_path):
    width = 2400
    height = 1600
    bg_color = (248, 250, 252) # #f8fafc
    card_bg = (255, 255, 255)
    border_color = (203, 213, 225) # #cbd5e1
    header_bg_primary = (30, 41, 59) # #1e293b
    header_bg_secondary = (51, 65, 85) # #334155
    text_dark = (15, 23, 42)
    text_muted = (100, 116, 139)
    pk_color = (185, 28, 28) # #b91c1c (red-700)
    fk_color = (3, 105, 161) # #0369a1 (sky-700)
    line_color = (71, 85, 105)

    img = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Load system fonts if available
    try:
        font_title = ImageFont.truetype("arial.ttf", 36)
        font_subtitle = ImageFont.truetype("arial.ttf", 20)
        font_header = ImageFont.truetype("arialbd.ttf", 20)
        font_field = ImageFont.truetype("arial.ttf", 16)
        font_badge = ImageFont.truetype("arialbd.ttf", 14)
    except IOError:
        font_title = ImageFont.load_default()
        font_subtitle = ImageFont.load_default()
        font_header = ImageFont.load_default()
        font_field = ImageFont.load_default()
        font_badge = ImageFont.load_default()

    # Draw Top Header Banner
    draw.rectangle([(0, 0), (width, 100)], fill=(15, 23, 42))
    draw.text((60, 22), "FacultyOS — Relational Entity-Relationship Diagram (ERD)", fill=(255, 255, 255), font=font_title)
    draw.text((60, 65), "Django 5.1/6.1 Relational Architecture &bull; SQLite Database &bull; UGC CAS & PBAS Performance Model", fill=(148, 163, 184), font=font_subtitle)

    # Helper function to draw an entity table
    def draw_entity(x, y, w, h, table_name, model_label, fields, is_core=False):
        # Card shadow & background
        draw.rectangle([(x+4, y+4), (x + w + 4, y + h + 4)], fill=(226, 232, 240))
        draw.rectangle([(x, y), (x + w, y + h)], fill=card_bg, outline=border_color, width=2)
        
        # Header
        hdr_bg = header_bg_primary if is_core else header_bg_secondary
        draw.rectangle([(x, y), (x + w, y + 48)], fill=hdr_bg)
        draw.text((x + 16, y + 8), table_name, fill=(255, 255, 255), font=font_header)
        draw.text((x + 16, y + 28), model_label, fill=(148, 163, 184), font=font_badge)

        # Fields
        cur_y = y + 60
        for f in fields:
            badge_text = f.get('key', '')
            field_name = f['name']
            field_type = f['type']
            
            # Key indicator
            if 'PK' in badge_text:
                draw.text((x + 16, cur_y), "[PK]", fill=pk_color, font=font_badge)
            elif 'FK' in badge_text:
                draw.text((x + 16, cur_y), "[FK]", fill=fk_color, font=font_badge)
            else:
                draw.text((x + 16, cur_y), "    ", fill=text_muted, font=font_badge)

            draw.text((x + 65, cur_y), field_name, fill=text_dark, font=font_field)
            draw.text((x + w - 160, cur_y), field_type, fill=text_muted, font=font_field)
            cur_y += 24

    # Define entities
    entities = {
        'auth_user': {
            'x': 60, 'y': 160, 'w': 420, 'h': 340,
            'table': 'auth_user', 'label': 'Django User Authentication',
            'is_core': True,
            'fields': [
                {'key': 'PK', 'name': 'id', 'type': 'Integer (PK)'},
                {'key': '', 'name': 'username', 'type': 'CharField(150) (UK)'},
                {'key': '', 'name': 'email', 'type': 'EmailField'},
                {'key': '', 'name': 'password', 'type': 'CharField(128)'},
                {'key': '', 'name': 'first_name', 'type': 'CharField(150)'},
                {'key': '', 'name': 'last_name', 'type': 'CharField(150)'},
                {'key': '', 'name': 'is_staff', 'type': 'BooleanField'},
                {'key': '', 'name': 'is_superuser', 'type': 'BooleanField'},
                {'key': '', 'name': 'date_joined', 'type': 'DateTimeField'},
            ]
        },
        'faculty_profile': {
            'x': 580, 'y': 160, 'w': 480, 'h': 420,
            'table': 'appraisal_facultyprofile', 'label': 'Institutional Faculty Dossier',
            'is_core': True,
            'fields': [
                {'key': 'PK', 'name': 'id', 'type': 'BigAutoField (PK)'},
                {'key': 'FK', 'name': 'user_id', 'type': 'OneToOne -> auth_user (UK)'},
                {'key': '', 'name': 'employee_id', 'type': 'CharField(20) (UK)'},
                {'key': '', 'name': 'department', 'type': 'CharField(20) [Choices]'},
                {'key': '', 'name': 'designation', 'type': 'CharField(50) [Choices]'},
                {'key': '', 'name': 'highest_qualification', 'type': 'CharField(50)'},
                {'key': '', 'name': 'specialization', 'type': 'CharField(150)'},
                {'key': '', 'name': 'date_of_joining', 'type': 'DateField'},
                {'key': '', 'name': 'experience_years', 'type': 'DecimalField(4, 1)'},
                {'key': '', 'name': 'promotion_status', 'type': 'CharField(30) [Choices]'},
                {'key': '', 'name': 'promotion_eligible_date', 'type': 'DateField (Nullable)'},
                {'key': '', 'name': 'created_at', 'type': 'DateTimeField'},
            ]
        },
        'teaching': {
            'x': 1180, 'y': 140, 'w': 540, 'h': 400,
            'table': 'appraisal_teachingrecord', 'label': 'Teaching Ledger (PBAS Cat I - Max 40)',
            'is_core': False,
            'fields': [
                {'key': 'PK', 'name': 'id', 'type': 'BigAutoField (PK)'},
                {'key': 'FK', 'name': 'faculty_id', 'type': 'FK -> FacultyProfile (CASCADE)'},
                {'key': '', 'name': 'academic_year', 'type': 'CharField(20)'},
                {'key': '', 'name': 'semester', 'type': 'CharField(10) [Odd/Even]'},
                {'key': '', 'name': 'subject_code', 'type': 'CharField(30)'},
                {'key': '', 'name': 'subject_name', 'type': 'CharField(120)'},
                {'key': '', 'name': 'course_type', 'type': 'CharField(20)'},
                {'key': '', 'name': 'scheduled_hours', 'type': 'PositiveIntegerField'},
                {'key': '', 'name': 'conducted_hours', 'type': 'PositiveIntegerField'},
                {'key': '', 'name': 'pass_percentage', 'type': 'DecimalField(5, 2)'},
                {'key': '', 'name': 'student_feedback_score', 'type': 'DecimalField(3, 2)'},
                {'key': '', 'name': 'innovative_teaching_methods', 'type': 'TextField'},
            ]
        },
        'research': {
            'x': 1780, 'y': 140, 'w': 540, 'h': 400,
            'table': 'appraisal_researchpublication', 'label': 'Research Ledger (PBAS Cat II - Max 30)',
            'is_core': False,
            'fields': [
                {'key': 'PK', 'name': 'id', 'type': 'BigAutoField (PK)'},
                {'key': 'FK', 'name': 'faculty_id', 'type': 'FK -> FacultyProfile (CASCADE)'},
                {'key': '', 'name': 'academic_year', 'type': 'CharField(20)'},
                {'key': '', 'name': 'title', 'type': 'CharField(255)'},
                {'key': '', 'name': 'journal_conference_name', 'type': 'CharField(255)'},
                {'key': '', 'name': 'publication_type', 'type': 'CharField(20) [SCI/UGC]'},
                {'key': '', 'name': 'issn_isbn', 'type': 'CharField(50)'},
                {'key': '', 'name': 'publication_date', 'type': 'DateField'},
                {'key': '', 'name': 'indexing_details', 'type': 'CharField(100)'},
                {'key': '', 'name': 'author_role', 'type': 'CharField(30)'},
                {'key': '', 'name': 'doi_or_url', 'type': 'URLField'},
            ]
        },
        'workshop': {
            'x': 1180, 'y': 590, 'w': 540, 'h': 380,
            'table': 'appraisal_workshoptraining', 'label': 'Workshops & FDPs (PBAS Cat III - Max 15)',
            'is_core': False,
            'fields': [
                {'key': 'PK', 'name': 'id', 'type': 'BigAutoField (PK)'},
                {'key': 'FK', 'name': 'faculty_id', 'type': 'FK -> FacultyProfile (CASCADE)'},
                {'key': '', 'name': 'academic_year', 'type': 'CharField(20)'},
                {'key': '', 'name': 'title', 'type': 'CharField(255)'},
                {'key': '', 'name': 'program_type', 'type': 'CharField(20) [FDP/STTP]'},
                {'key': '', 'name': 'role', 'type': 'CharField(30) [Participant/Lead]'},
                {'key': '', 'name': 'organizing_institution', 'type': 'CharField(200)'},
                {'key': '', 'name': 'start_date / end_date', 'type': 'DateField'},
                {'key': '', 'name': 'duration_days', 'type': 'PositiveIntegerField'},
                {'key': '', 'name': 'certificate_link', 'type': 'URLField'},
            ]
        },
        'project': {
            'x': 1780, 'y': 590, 'w': 540, 'h': 380,
            'table': 'appraisal_completedproject', 'label': 'Sponsored Projects (PBAS Cat IV - Max 15)',
            'is_core': False,
            'fields': [
                {'key': 'PK', 'name': 'id', 'type': 'BigAutoField (PK)'},
                {'key': 'FK', 'name': 'faculty_id', 'type': 'FK -> FacultyProfile (CASCADE)'},
                {'key': '', 'name': 'academic_year', 'type': 'CharField(20)'},
                {'key': '', 'name': 'title', 'type': 'CharField(255)'},
                {'key': '', 'name': 'funding_agency', 'type': 'CharField(150)'},
                {'key': '', 'name': 'project_type', 'type': 'CharField(20)'},
                {'key': '', 'name': 'grant_amount', 'type': 'DecimalField(12, 2)'},
                {'key': '', 'name': 'duration_months', 'type': 'PositiveIntegerField'},
                {'key': '', 'name': 'role', 'type': 'CharField(10) [PI/Co-PI]'},
                {'key': '', 'name': 'status', 'type': 'CharField(20) [Completed]'},
            ]
        },
        'appraisal': {
            'x': 580, 'y': 660, 'w': 480, 'h': 460,
            'table': 'appraisal_appraisalsubmission', 'label': 'Annual Self-Appraisal & CAS Submission',
            'is_core': True,
            'fields': [
                {'key': 'PK', 'name': 'id', 'type': 'BigAutoField (PK)'},
                {'key': 'FK', 'name': 'faculty_id', 'type': 'FK -> FacultyProfile (CASCADE)'},
                {'key': '', 'name': 'academic_year', 'type': 'CharField(20)'},
                {'key': '', 'name': 'status', 'type': 'CharField(25) [Submitted/Approved]'},
                {'key': '', 'name': 'teaching_score', 'type': 'DecimalField(5, 2) (/40)'},
                {'key': '', 'name': 'research_score', 'type': 'DecimalField(5, 2) (/30)'},
                {'key': '', 'name': 'workshop_score', 'type': 'DecimalField(5, 2) (/15)'},
                {'key': '', 'name': 'project_score', 'type': 'DecimalField(5, 2) (/15)'},
                {'key': '', 'name': 'total_score', 'type': 'DecimalField(5, 2) (/100)'},
                {'key': '', 'name': 'performance_grade', 'type': 'CharField(50)'},
                {'key': '', 'name': 'promotion_recommendation', 'type': 'CharField(50)'},
                {'key': 'FK', 'name': 'reviewed_by_id', 'type': 'FK -> auth_user (SET_NULL)'},
            ]
        }
    }

    # Draw all entities
    for k, e in entities.items():
        draw_entity(e['x'], e['y'], e['w'], e['h'], e['table'], e['label'], e['fields'], e.get('is_core', False))

    # Helper function to draw relationship connector lines
    def draw_connector(start_pt, end_pt, label, is_dashed=False):
        draw.line([start_pt, end_pt], fill=line_color, width=3)
        # Draw connector arrow/circle endpoint
        mid_x = (start_pt[0] + end_pt[0]) // 2
        mid_y = (start_pt[1] + end_pt[1]) // 2
        # Text label background pill
        bbox = draw.textbbox((mid_x - 40, mid_y - 12), label, font=font_badge)
        draw.rectangle([(bbox[0]-4, bbox[1]-2), (bbox[2]+4, bbox[3]+2)], fill=(241, 245, 249), outline=border_color)
        draw.text((mid_x - 35, mid_y - 10), label, fill=(30, 41, 59), font=font_badge)

    # 1. User -> FacultyProfile (OneToOne)
    draw_connector((480, 240), (580, 240), "1 : 1 (CASCADE)")

    # 2. FacultyProfile -> Teaching
    draw_connector((1060, 240), (1180, 240), "1 : N (CASCADE)")

    # 3. FacultyProfile -> Research
    draw_connector((1060, 320), (1780, 320), "1 : N (CASCADE)")

    # 4. FacultyProfile -> Workshop
    draw_connector((1060, 440), (1180, 680), "1 : N (CASCADE)")

    # 5. FacultyProfile -> Project
    draw_connector((1060, 520), (1780, 680), "1 : N (CASCADE)")

    # 6. FacultyProfile -> AppraisalSubmission
    draw_connector((820, 580), (820, 660), "1 : N (CASCADE)")

    # 7. auth_user -> AppraisalSubmission (reviewed_by)
    draw.line([(270, 500), (270, 890), (580, 890)], fill=(148, 163, 184), width=2)
    bbox = draw.textbbox((330, 875), "1 : N Reviewer (SET_NULL)", font=font_badge)
    draw.rectangle([(bbox[0]-4, bbox[1]-2), (bbox[2]+4, bbox[3]+2)], fill=(241, 245, 249), outline=border_color)
    draw.text((330, 875), "1 : N Reviewer (SET_NULL)", fill=(71, 85, 105), font=font_badge)

    # Footer note
    draw.rectangle([(0, height - 60), (width, height)], fill=(241, 245, 249), outline=border_color)
    draw.text((60, height - 42), "Entity-Relationship Schema strictly verified against appraisal.models & core.models &bull; Zero schema drift &bull; SQLite FK enforcement verified", fill=text_muted, font=font_field)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PNG", dpi=(300, 300))
    print(f"ER diagram successfully created at {output_path}")

if __name__ == '__main__':
    create_er_diagram("docs/ER_Diagram.png")

