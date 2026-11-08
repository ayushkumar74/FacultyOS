import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)


def generate_appraisal_pdf(appraisal):
    """
    Generates a professional academic PDF appraisal report for a faculty member.
    Returns a BytesIO buffer.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36,
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#1E3A8A'), # Navy blue
        alignment=1, # Center
        fontName='Helvetica-Bold',
        spaceAfter=4,
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#4B5563'),
        alignment=1,
        fontName='Helvetica',
        spaceAfter=12,
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E3A8A'),
        fontName='Helvetica-Bold',
        spaceBefore=10,
        spaceAfter=6,
    )

    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontSize=9,
        leading=12,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#111827'),
    )

    cell_text = ParagraphStyle(
        'CellText',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        fontName='Helvetica',
        textColor=colors.HexColor('#374151'),
    )

    header_cell = ParagraphStyle(
        'HeaderCell',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        alignment=1,
    )

    story = []

    # 1. Header & Title
    story.append(Paragraph("NATIONAL INSTITUTE OF TECHNOLOGY & HIGHER EDUCATION", title_style))
    story.append(Paragraph(
        f"ANNUAL FACULTY SELF-APPRAISAL & PERFORMANCE REPORT — ACADEMIC YEAR {appraisal.academic_year}",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1E3A8A'), spaceAfter=12))

    # 2. Faculty Profile Information
    faculty = appraisal.faculty
    profile_data = [
        [
            Paragraph("Faculty Name:", cell_bold),
            Paragraph(faculty.user.get_full_name() or faculty.user.username, cell_text),
            Paragraph("Employee ID:", cell_bold),
            Paragraph(faculty.employee_id, cell_text),
        ],
        [
            Paragraph("Department:", cell_bold),
            Paragraph(faculty.get_department_display(), cell_text),
            Paragraph("Designation:", cell_bold),
            Paragraph(faculty.designation, cell_text),
        ],
        [
            Paragraph("Highest Qualification:", cell_bold),
            Paragraph(faculty.highest_qualification, cell_text),
            Paragraph("Specialization:", cell_bold),
            Paragraph(faculty.specialization or "N/A", cell_text),
        ],
        [
            Paragraph("Date of Joining:", cell_bold),
            Paragraph(str(faculty.date_of_joining), cell_text),
            Paragraph("Experience (Years):", cell_bold),
            Paragraph(f"{faculty.experience_years} Years", cell_text),
        ],
        [
            Paragraph("Contact Email:", cell_bold),
            Paragraph(faculty.user.email or "N/A", cell_text),
            Paragraph("Contact Phone:", cell_bold),
            Paragraph(faculty.contact_number or "N/A", cell_text),
        ],
    ]

    profile_table = Table(profile_data, colWidths=[120, 140, 120, 140])
    profile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(profile_table)
    story.append(Spacer(1, 10))

    # 3. Overall Performance Score & Appraisal Summary
    status_color = colors.HexColor('#059669') if appraisal.status == 'APPROVED' else (
        colors.HexColor('#DC2626') if appraisal.status == 'REJECTED' else colors.HexColor('#D97706')
    )

    score_summary_data = [
        [
            Paragraph("Teaching Score<br/><b>" + str(appraisal.teaching_score) + " / 40</b>", header_cell),
            Paragraph("Research Score<br/><b>" + str(appraisal.research_score) + " / 30</b>", header_cell),
            Paragraph("Workshops Score<br/><b>" + str(appraisal.workshop_score) + " / 15</b>", header_cell),
            Paragraph("Projects Score<br/><b>" + str(appraisal.project_score) + " / 15</b>", header_cell),
            Paragraph("Total Score<br/><b>" + str(appraisal.total_score) + " / 100</b>", header_cell),
        ],
        [
            Paragraph("<b>Overall Grade:</b> " + appraisal.performance_grade, cell_text),
            Paragraph("<b>Appraisal Status:</b> " + appraisal.get_status_display(), cell_text),
            Paragraph("<b>Promotion Recommendation:</b> " + appraisal.get_promotion_recommendation_display(), cell_text),
            Paragraph("<b>Submitted On:</b> " + appraisal.submission_date.strftime("%d-%b-%Y"), cell_text),
            Paragraph("<b>Reviewed On:</b> " + (appraisal.reviewed_at.strftime("%d-%b-%Y") if appraisal.reviewed_at else "Pending"), cell_text),
        ]
    ]

    score_table = Table(score_summary_data, colWidths=[104, 104, 104, 104, 104])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#EFF6FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1E3A8A')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BFDBFE')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('SPAN', (0, 1), (0, 1)),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 10))

    # 4. Teaching Performance Records
    story.append(Paragraph("1. Teaching & Learning Performance", section_heading))
    teaching_records = faculty.teaching_records.filter(academic_year=appraisal.academic_year)
    if teaching_records.exists():
        teach_headers = [
            Paragraph("Code & Subject", header_cell),
            Paragraph("Sem", header_cell),
            Paragraph("Sched/Cond Hours", header_cell),
            Paragraph("Compliance %", header_cell),
            Paragraph("Pass %", header_cell),
            Paragraph("Student Rating", header_cell),
        ]
        teach_rows = [teach_headers]
        for tr in teaching_records:
            teach_rows.append([
                Paragraph(f"<b>{tr.subject_code}</b>: {tr.subject_name}", cell_text),
                Paragraph(tr.semester, cell_text),
                Paragraph(f"{tr.scheduled_hours} / {tr.conducted_hours} hrs", cell_text),
                Paragraph(f"{tr.compliance_rate}%", cell_text),
                Paragraph(f"{tr.pass_percentage}%", cell_text),
                Paragraph(f"{tr.student_feedback_score} / 5.0", cell_text),
            ])
        t_table = Table(teach_rows, colWidths=[160, 50, 90, 75, 65, 80])
        t_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(t_table)
    else:
        story.append(Paragraph("<i>No teaching records submitted for this session.</i>", cell_text))
    story.append(Spacer(1, 8))

    # 5. Research Publications
    story.append(Paragraph("2. Research Publications & Intellectual Property", section_heading))
    pub_records = faculty.research_publications.filter(academic_year=appraisal.academic_year)
    if pub_records.exists():
        pub_headers = [
            Paragraph("Publication Title & Details", header_cell),
            Paragraph("Type / Indexing", header_cell),
            Paragraph("Role", header_cell),
            Paragraph("Date / ISSN", header_cell),
        ]
        pub_rows = [pub_headers]
        for pr in pub_records:
            details = f"<b>{pr.title}</b><br/><i>{pr.journal_conference_name}</i>"
            if pr.doi_or_url:
                details += f"<br/>Link: {pr.doi_or_url}"
            pub_rows.append([
                Paragraph(details, cell_text),
                Paragraph(f"{pr.get_publication_type_display()}<br/>{pr.indexing_details or ''}", cell_text),
                Paragraph(pr.author_role, cell_text),
                Paragraph(f"{pr.publication_date.strftime('%b %Y')}<br/>{pr.issn_isbn or ''}", cell_text),
            ])
        p_table = Table(pub_rows, colWidths=[240, 130, 75, 75])
        p_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(p_table)
    else:
        story.append(Paragraph("<i>No research publications registered for this session.</i>", cell_text))
    story.append(Spacer(1, 8))

    # 6. Workshops & Professional Development
    story.append(Paragraph("3. Workshops, FDPs & Training Attended", section_heading))
    workshops = faculty.workshops_trainings.filter(academic_year=appraisal.academic_year)
    if workshops.exists():
        ws_headers = [
            Paragraph("Program Title", header_cell),
            Paragraph("Type", header_cell),
            Paragraph("Role", header_cell),
            Paragraph("Organizing Body", header_cell),
            Paragraph("Days", header_cell),
        ]
        ws_rows = [ws_headers]
        for w in workshops:
            ws_rows.append([
                Paragraph(f"<b>{w.title}</b>", cell_text),
                Paragraph(w.get_program_type_display(), cell_text),
                Paragraph(w.role, cell_text),
                Paragraph(w.organizing_institution, cell_text),
                Paragraph(f"{w.duration_days} Days", cell_text),
            ])
        w_table = Table(ws_rows, colWidths=[180, 110, 80, 110, 40])
        w_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(w_table)
    else:
        story.append(Paragraph("<i>No workshop records submitted for this session.</i>", cell_text))
    story.append(Spacer(1, 8))

    # 7. Completed Projects & Consultancy
    story.append(Paragraph("4. Sponsored Research & Consultancy Projects", section_heading))
    projects = faculty.completed_projects.filter(academic_year=appraisal.academic_year)
    if projects.exists():
        proj_headers = [
            Paragraph("Project Title", header_cell),
            Paragraph("Agency", header_cell),
            Paragraph("Type", header_cell),
            Paragraph("Grant (INR)", header_cell),
            Paragraph("Role / Status", header_cell),
        ]
        proj_rows = [proj_headers]
        for p in projects:
            proj_rows.append([
                Paragraph(f"<b>{p.title}</b>", cell_text),
                Paragraph(p.funding_agency, cell_text),
                Paragraph(p.get_project_type_display(), cell_text),
                Paragraph(f"Rs. {p.grant_amount:,.2f}", cell_text),
                Paragraph(f"{p.get_role_display()}<br/>({p.status})", cell_text),
            ])
        pr_table = Table(proj_rows, colWidths=[180, 100, 100, 75, 65])
        pr_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#334155')),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#94A3B8')),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ]))
        story.append(pr_table)
    else:
        story.append(Paragraph("<i>No project records submitted for this session.</i>", cell_text))
    story.append(Spacer(1, 10))

    # 8. Remarks & Committee Assessment
    remarks_data = [
        [
            Paragraph("<b>Faculty Self-Appraisal Remarks:</b><br/>" + (appraisal.faculty_remarks or "No remarks provided."), cell_text)
        ],
        [
            Paragraph("<b>Reviewer / Appraisal Committee Remarks:</b><br/>" + (appraisal.admin_remarks or "Review evaluation pending."), cell_text)
        ]
    ]
    remarks_table = Table(remarks_data, colWidths=[520])
    remarks_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(remarks_table)
    story.append(Spacer(1, 20))

    # 9. Signatures Block
    sig_data = [
        [
            Paragraph("____________________________<br/><b>Faculty Signature</b><br/>Date: " + appraisal.submission_date.strftime("%d-%b-%Y"), cell_text),
            Paragraph("____________________________<br/><b>Head of Department / Dean</b><br/>Date: " + (appraisal.reviewed_at.strftime("%d-%b-%Y") if appraisal.reviewed_at else "___________"), cell_text),
            Paragraph("____________________________<br/><b>Registrar / Vice Chancellor</b><br/>Seal & Approval", cell_text),
        ]
    ]
    sig_table = Table(sig_data, colWidths=[173, 173, 174])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(KeepTogether([sig_table]))

    doc.build(story)
    buffer.seek(0)
    return buffer

