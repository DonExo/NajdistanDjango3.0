from functools import wraps
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse


# A CBV decorator to allow only Ajax requests
def ajax_required(view):
    @wraps(view)
    def _wrapped_view(request, *args, **kwargs):
        if request.is_ajax():
            return view(request, *args, **kwargs)
        else:
            return JsonResponse({'error': 'Non-Ajax request detected'}, status=403)
    return _wrapped_view
