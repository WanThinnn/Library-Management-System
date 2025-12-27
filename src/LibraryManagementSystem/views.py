"""
Custom error handlers for LibraryManagementSystem.
"""
from django.shortcuts import render


def bad_request(request, exception=None):
    """Handle 400 Bad Request errors."""
    return render(request, 'errors/400.html', status=400)


def permission_denied(request, exception=None):
    """Handle 403 Forbidden errors."""
    return render(request, 'errors/403.html', status=403)


def page_not_found(request, exception=None):
    """Handle 404 Not Found errors."""
    return render(request, 'errors/404.html', status=404)


def server_error(request):
    """Handle 500 Internal Server errors."""
    return render(request, 'errors/500.html', status=500)
