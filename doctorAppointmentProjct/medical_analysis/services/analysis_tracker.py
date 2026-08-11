from django.core.cache import cache
from django.utils import timezone
import json
import uuid


class AnalysisTracker:
    def __init__(self):
        self.cache_timeout = 3600  # 1 hour

    def start_analysis(self, user_id, analysis_type):
        """Start tracking an analysis"""
        task_id = str(uuid.uuid4())
        status = {
            'task_id': task_id,
            'user_id': user_id,
            'analysis_type': analysis_type,
            'status': 'processing',
            'progress': 0,
            'message': 'Starting analysis...',
            'started_at': timezone.now().isoformat(),
        }

        cache.set(f'analysis_{task_id}', json.dumps(status), self.cache_timeout)
        return task_id

    def update_progress(self, task_id, progress, message):
        """Update analysis progress"""
        status_json = cache.get(f'analysis_{task_id}')
        if status_json:
            status = json.loads(status_json)
            status['progress'] = progress
            status['message'] = message
            status['updated_at'] = timezone.now().isoformat()
            cache.set(f'analysis_{task_id}', json.dumps(status), self.cache_timeout)

    def complete_analysis(self, task_id, result=None, error=None):
        """Mark analysis as complete"""
        status_json = cache.get(f'analysis_{task_id}')
        if status_json:
            status = json.loads(status_json)
            status['status'] = 'completed' if not error else 'error'
            status['progress'] = 100
            status['message'] = 'Analysis completed' if not error else f'Error: {error}'
            status['completed_at'] = timezone.now().isoformat()
            if result:
                status['result'] = result
            cache.set(f'analysis_{task_id}', json.dumps(status), self.cache_timeout)

    def get_status(self, task_id):
        """Get current analysis status"""
        status_json = cache.get(f'analysis_{task_id}')
        return json.loads(status_json) if status_json else None


# Initialize tracker
analysis_tracker = AnalysisTracker()