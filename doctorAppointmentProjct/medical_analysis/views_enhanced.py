

import analysis
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .tasks import process_image_analysis_async, process_text_analysis_async
from .services.analysis_tracker import analysis_tracker
import json


@csrf_exempt
@require_http_methods(["POST"])
def start_async_analysis(request):
    """Start asynchronous analysis"""
    try:
        data = json.loads(request.body)
        analysis_type = data.get('type')  # 'image' or 'text'

        if analysis_type == 'image':
            # Handle image upload and create analysis record
            # ... (similar to existing image_analysis_view)

            # Start async task
            task_id = analysis_tracker.start_analysis(request.user.id, 'image')
            process_image_analysis_async.delay(analysis.id, task_id)

        elif analysis_type == 'text':
            # Handle text analysis
            # ... (similar to existing text_analysis_view)

            # Start async task
            task_id = analysis_tracker.start_analysis(request.user.id, 'text')
            process_text_analysis_async.delay(analysis.id, task_id)

        return JsonResponse({
            'status': 'started',
            'task_id': task_id,
            'analysis_id': str(analysis.id)
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def check_analysis_status(request, task_id):
    """Check analysis progress"""
    status = analysis_tracker.get_status(task_id)
    if status:
        return JsonResponse(status)
    else:
        return JsonResponse({'error': 'Task not found'}, status=404)