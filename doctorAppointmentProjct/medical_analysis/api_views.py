from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.files.base import ContentFile
import base64
import uuid

from medical_analysis.models import MedicalAnalysis
from medical_analysis.services.analysis_tracker import analysis_tracker


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mobile_image_analysis(request, process_image_analysis_async=None):
    """Mobile API for image analysis"""
    try:
        # Get base64 image data
        image_data = request.data.get('image_data')
        symptoms = request.data.get('symptoms', '')

        if not image_data:
            return Response(
                {'error': 'Image data is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Decode base64 image
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        image_file = ContentFile(
            base64.b64decode(imgstr),
            name=f'{uuid.uuid4()}.{ext}'
        )

        # Create analysis record
        analysis = MedicalAnalysis.objects.create(
            user=request.user,
            analysis_type='image',
            symptoms_text=symptoms,
            uploaded_image=image_file
        )

        # Start async analysis
        task_id = analysis_tracker.start_analysis(request.user.id, 'image')
        process_image_analysis_async.delay(analysis.id, task_id)

        return Response({
            'task_id': task_id,
            'analysis_id': str(analysis.id),
            'status': 'processing'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mobile_analysis_result(request, analysis_id):
    """Get analysis results for mobile"""
    try:
        analysis = MedicalAnalysis.objects.get(
            id=analysis_id,
            user=request.user
        )

        result_data = {
            'id': str(analysis.id),
            'type': analysis.analysis_type,
            'created_at': analysis.created_at,
            'confidence_score': analysis.confidence_score,
            'symptoms': analysis.symptoms_text,
            'result': analysis.analysis_result,
        }

        if analysis.uploaded_image:
            result_data['image_url'] = request.build_absolute_uri(
                analysis.uploaded_image.url
            )

        return Response(result_data, status=status.HTTP_200_OK)

    except MedicalAnalysis.DoesNotExist:
        return Response(
            {'error': 'Analysis not found'},
            status=status.HTTP_404_NOT_FOUND
        )