from django.urls import path
from . import views

urlpatterns = [
    # Faculty Portal Routes
    path('faculty/dashboard/', views.faculty_dashboard, name='faculty_dashboard'),
    path('faculty/profile/', views.faculty_profile_view, name='faculty_profile'),
    path('faculty/profile/edit/', views.faculty_profile_update, name='faculty_profile_update'),

    # Teaching Records
    path('faculty/teaching/', views.teaching_list, name='teaching_list'),
    path('faculty/teaching/add/', views.teaching_create, name='teaching_create'),
    path('faculty/teaching/<int:pk>/edit/', views.teaching_update, name='teaching_update'),
    path('faculty/teaching/<int:pk>/delete/', views.teaching_delete, name='teaching_delete'),

    # Research Publications
    path('faculty/research/', views.research_list, name='research_list'),
    path('faculty/research/add/', views.research_create, name='research_create'),
    path('faculty/research/<int:pk>/edit/', views.research_update, name='research_update'),
    path('faculty/research/<int:pk>/delete/', views.research_delete, name='research_delete'),

    # Workshops & Training
    path('faculty/workshops/', views.workshop_list, name='workshop_list'),
    path('faculty/workshops/add/', views.workshop_create, name='workshop_create'),
    path('faculty/workshops/<int:pk>/edit/', views.workshop_update, name='workshop_update'),
    path('faculty/workshops/<int:pk>/delete/', views.workshop_delete, name='workshop_delete'),

    # Sponsored Projects
    path('faculty/projects/', views.project_list, name='project_list'),
    path('faculty/projects/add/', views.project_create, name='project_create'),
    path('faculty/projects/<int:pk>/edit/', views.project_update, name='project_update'),
    path('faculty/projects/<int:pk>/delete/', views.project_delete, name='project_delete'),

    # Appraisal Submission & Reports
    path('faculty/appraisal/submit/', views.submit_appraisal, name='submit_appraisal'),
    path('faculty/appraisal/<int:pk>/', views.appraisal_detail, name='appraisal_detail'),
    path('faculty/appraisal/<int:pk>/pdf/', views.download_appraisal_pdf, name='download_appraisal_pdf'),

    # Admin Portal Routes
    path('admin-portal/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-portal/faculty/', views.admin_faculty_list, name='admin_faculty_list'),
    path('admin-portal/faculty/export-csv/', views.admin_export_faculty_csv, name='admin_export_faculty_csv'),
    path('admin-portal/faculty/<int:pk>/', views.admin_faculty_detail, name='admin_faculty_detail'),
    path('admin-portal/faculty/<int:pk>/promotion/', views.admin_update_promotion, name='admin_update_promotion'),
    path('admin-portal/appraisals/', views.admin_appraisals_list, name='admin_appraisals_list'),
    path('admin-portal/appraisals/export-csv/', views.admin_export_appraisals_csv, name='admin_export_appraisals_csv'),
    path('admin-portal/appraisals/<int:pk>/review/', views.admin_appraisal_review, name='admin_appraisal_review'),
    path('admin-portal/appraisals/<int:pk>/pdf/', views.admin_download_pdf, name='admin_download_pdf'),
]

