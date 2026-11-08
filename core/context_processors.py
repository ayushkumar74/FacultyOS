from django.utils import timezone

def portal_context(request):
    """
    Global context processor for portal templates.
    Provides academic year, role helpers, and faculty profile if available.
    """
    context = {
        'portal_name': 'Faculty Self-Appraisal & Career Advancement Portal',
        'current_academic_year': '2025-2026',
        'is_admin_user': False,
        'user_faculty_profile': None,
    }
    
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            context['is_admin_user'] = True
        
        # Check if the user has an associated faculty profile
        if hasattr(request.user, 'faculty_profile'):
            context['user_faculty_profile'] = request.user.faculty_profile
            
    return context

