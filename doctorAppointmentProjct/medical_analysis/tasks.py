from celery import shared_task
from .models import MedicalAnalysis
from .services.groq_service import groq_service
from .services.analysis_tracker import analysis_tracker
from django.conf import settings
import os


@shared_task
def process_image_analysis_async(analysis_id, task_id):
    """Process image analysis asynchronously"""
    try:
        analysis = MedicalAnalysis.objects.get(id=analysis_id)

        # Update progress
        analysis_tracker.update_progress(task_id, 25, "Processing image...")

        # Get full image path
        full_path = os.path.join(settings.MEDIA_ROOT, str(analysis.uploaded_image))

        # Update progress
        analysis_tracker.update_progress(task_id, 50, "Analyzing with AI...")

        # Perform Groq analysis
        analysis_result = groq_service.analyze_medical_image(
            full_path,
            analysis.symptoms_text
        )

        # Update progress
        analysis_tracker.update_progress(task_id, 75, "Processing results...")

        # Update analysis with results
        analysis.analysis_result = analysis_result
        if 'possible_conditions' in analysis_result and analysis_result['possible_conditions']:
            confidence_str = analysis_result['possible_conditions'][0].get('confidence', '0%')
            analysis.confidence_score = float(confidence_str.rstrip('%')) / 100
        analysis.save()

        # Complete analysis
        analysis_tracker.complete_analysis(task_id, result=analysis_result)

        return {"status": "success", "analysis_id": str(analysis_id)}

    except Exception as e:
        analysis_tracker.complete_analysis(task_id, error=str(e))
        return {"status": "error", "error": str(e)}


@shared_task
def process_text_analysis_async(analysis_id, task_id):
    """Process text analysis asynchronously"""
    try:
        analysis = MedicalAnalysis.objects.get(id=analysis_id)

        # Update progress
        analysis_tracker.update_progress(task_id, 30, "Analyzing symptoms...")

        # Perform Groq analysis
        analysis_result = groq_service.analyze_symptoms(analysis.symptoms_text)

        # Update progress
        analysis_tracker.update_progress(task_id, 80, "Processing results...")

        # Update analysis with results
        analysis.analysis_result = analysis_result
        if 'possible_conditions' in analysis_result and analysis_result['possible_conditions']:
            probability_str = analysis_result['possible_conditions'][0].get('probability', '0%')
            analysis.confidence_score = float(probability_str.rstrip('%')) / 100
        analysis.save()

        # Complete analysis
        analysis_tracker.complete_analysis(task_id)

        return {"status": "success", "analysis_id": str(analysis_id)}

    except Exception as e:
        analysis_tracker.complete_analysis(task_id, error=str(e))
        return {"status": "error", "error": str(e)}