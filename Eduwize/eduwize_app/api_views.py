from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Notification

@login_required
@require_POST
def mark_notification_as_read(request, notification_id):
    """
    Mark a notification as read via AJAX
    """
    try:
        notification = get_object_or_404(Notification, id=notification_id)
        
        # Check if the notification belongs to the current user
        if notification.student != request.user.student:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        
        notification.is_read = True
        notification.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def mark_notification_as_unread(request, notification_id):
    """
    Mark a notification as unread via AJAX
    """
    try:
        notification = get_object_or_404(Notification, id=notification_id)
        
        # Check if the notification belongs to the current user
        if notification.student != request.user.student:
            return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
        
        notification.is_read = False
        notification.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@login_required
@require_POST
def mark_all_notifications_as_read(request):
    """
    Mark all notifications as read via AJAX
    """
    try:
        # Get all unread notifications for this user
        unread_notifications = Notification.objects.filter(
            student=request.user.student,
            is_read=False
        )
        
        # Mark them all as read
        unread_notifications.update(is_read=True)
        
        return JsonResponse({'success': True, 'count': unread_notifications.count()})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
