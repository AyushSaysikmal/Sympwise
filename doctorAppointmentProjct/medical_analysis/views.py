from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.files.storage import default_storage
from django.conf import settings
import json
import os
from .models import MedicalAnalysis, ChatSession, ChatMessage, PDFReport
from .services.groq_service import groq_service
from .utils.pdf_generator import generate_medical_report


@login_required
def dashboard(request):
    """Main dashboard view"""
    recent_analyses = MedicalAnalysis.objects.filter(user=request.user)[:5]
    active_chats = ChatSession.objects.filter(user=request.user, is_active=True)[:3]

    context = {
        'recent_analyses': recent_analyses,
        'active_chats': active_chats,
        'total_analyses': MedicalAnalysis.objects.filter(user=request.user).count(),
    }
    return render(request, 'medical_analysis/dashboard.html', context)


def normalize_analysis_result(analysis_result):
    """
    Normalize analysis result fields for template consistency.
    Handles different field names from different analysis types.
    """
    if not isinstance(analysis_result, dict):
        return analysis_result

    # Normalize condition fields
    if 'possible_conditions' in analysis_result:
        for condition in analysis_result['possible_conditions']:
            # Ensure both probability and confidence exist
            if 'probability' in condition and 'confidence' not in condition:
                condition['confidence'] = condition['probability']
            elif 'confidence' in condition and 'probability' not in condition:
                condition['probability'] = condition['confidence']

            # Ensure both description and reasoning exist
            if 'description' in condition and 'reasoning' not in condition:
                condition['reasoning'] = condition['description']
            elif 'reasoning' in condition and 'description' not in condition:
                condition['description'] = condition['reasoning']

    # Normalize top-level fields - create BOTH versions for maximum compatibility

    # Severity field normalization
    if 'severity' in analysis_result and 'severity_assessment' not in analysis_result:
        analysis_result['severity_assessment'] = analysis_result['severity']
    elif 'severity_assessment' in analysis_result and 'severity' not in analysis_result:
        analysis_result['severity'] = analysis_result['severity_assessment']

    # Immediate attention field normalization
    if 'immediate_attention_needed' in analysis_result and 'urgent_care_needed' not in analysis_result:
        analysis_result['urgent_care_needed'] = analysis_result['immediate_attention_needed']
    elif 'urgent_care_needed' in analysis_result and 'immediate_attention_needed' not in analysis_result:
        analysis_result['immediate_attention_needed'] = analysis_result['urgent_care_needed']

    return analysis_result



@login_required
def image_analysis_view(request):
    """Handle image-based medical analysis"""
    if request.method == 'POST':
        try:
            symptoms = request.POST.get('symptoms', '')
            uploaded_file = request.FILES.get('medical_image')

            if not uploaded_file:
                messages.error(request, 'Please upload an image for analysis.')
                return render(request, 'medical_analysis/image_analysis.html')

            # Save the uploaded file
            file_path = default_storage.save(
                f'medical_images/{uploaded_file.name}',
                uploaded_file
            )
            full_path = os.path.join(settings.MEDIA_ROOT, file_path)

            # Create analysis record
            analysis = MedicalAnalysis.objects.create(
                user=request.user,
                analysis_type='image',
                symptoms_text=symptoms,
                uploaded_image=file_path
            )

            # Perform Groq analysis
            analysis_result = groq_service.analyze_medical_image(full_path, symptoms)

            # Normalize field names for template consistency
            analysis_result = normalize_analysis_result(analysis_result)

            # Update analysis with results
            analysis.analysis_result = analysis_result
            if 'possible_conditions' in analysis_result:
                analysis.confidence_score = float(
                    analysis_result['possible_conditions'][0].get('confidence', '0').rstrip('%')
                ) / 100 if analysis_result['possible_conditions'] else 0.0
            analysis.save()

            messages.success(request, 'Image analysis completed successfully!')
            return redirect('analysis_results', analysis_id=analysis.id)

        except Exception as e:
            messages.error(request, f'Analysis failed: {str(e)}')
            return render(request, 'medical_analysis/image_analysis.html')

    return render(request, 'medical_analysis/image_analysis.html')


@login_required
def analysis_results(request, analysis_id):
    """Display analysis results"""
    analysis = get_object_or_404(MedicalAnalysis, id=analysis_id, user=request.user)
    context = {'analysis': analysis}
    return render(request, 'medical_analysis/results.html', context)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def ai_assistant_chat(request, session_id=None):
    """AI Assistant chat interface - works for both authenticated and anonymous users"""

    # Determine user for session creation
    user = request.user if request.user.is_authenticated else None
    session_key = request.session.session_key if not user else None

    # Ensure session key exists for anonymous users
    if not user and not session_key:
        request.session.create()
        session_key = request.session.session_key

    if request.method == 'GET':
        # Get or create chat session
        if session_id:
            try:
                if user:
                    # For authenticated users, check user ownership
                    session = ChatSession.objects.get(id=session_id, user=user)
                else:
                    # For anonymous users, check session_key ownership
                    session = ChatSession.objects.get(
                        id=session_id,
                        user=None,
                        session_key=session_key
                    )
            except ChatSession.DoesNotExist:
                # Create new session if not found or not owned by current user
                session = ChatSession.objects.create(
                    user=user,
                    session_key=session_key
                )
                return redirect('ai_assistant_chat', session_id=session.id)
        else:
            # Create new session
            session = ChatSession.objects.create(
                user=user,
                session_key=session_key
            )
            return redirect('ai_assistant_chat', session_id=session.id)

        messages = session.messages.all()

        # Get user sessions based on authentication status
        if user:
            user_sessions = ChatSession.objects.filter(user=user, is_active=True)
        else:
            # For anonymous users, get sessions by session_key
            user_sessions = ChatSession.objects.filter(
                user=None,
                session_key=session_key,
                is_active=True
            )

        context = {
            'session': session,
            'messages': messages,
            'user_sessions': user_sessions,
            'is_authenticated': request.user.is_authenticated
        }
        return render(request, 'medical_analysis/ai_assistant.html', context)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()

            if not user_message:
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)

            # Verify session ownership
            try:
                if user:
                    # Authenticated user
                    session = ChatSession.objects.get(id=session_id, user=user)
                else:
                    # Anonymous user - check session_key ownership
                    session = ChatSession.objects.get(
                        id=session_id,
                        user=None,
                        session_key=session_key
                    )
            except ChatSession.DoesNotExist:
                return JsonResponse({'error': 'Session not found'}, status=404)

            # Save user message
            user_msg = ChatMessage.objects.create(
                session=session,
                message_type='user',
                content=user_message
            )

            # Get conversation history
            recent_messages = list(session.messages.values('message_type', 'content'))[-10:]
            conversation_history = [
                {"role": msg['message_type'] if msg['message_type'] != 'assistant' else 'assistant',
                 "content": msg['content']}
                for msg in recent_messages[:-1]  # Exclude the just-added user message
            ]

            # Get AI response
            ai_response = groq_service.get_ai_assistant_response(
                user_message,
                conversation_history
            )

            # Save AI response
            ai_msg = ChatMessage.objects.create(
                session=session,
                message_type='assistant',
                content=ai_response
            )

            return JsonResponse({
                'success': True,
                'response': ai_response,
                'timestamp': ai_msg.timestamp.isoformat()
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


@login_required
def generate_pdf_report(request, analysis_id):
    """Generate PDF report for analysis - Always fresh generation"""
    analysis = get_object_or_404(MedicalAnalysis, id=analysis_id, user=request.user)

    try:
        # Always remove existing PDF to force fresh generation
        if hasattr(analysis, 'pdf_report'):
            old_pdf = analysis.pdf_report
            if os.path.exists(old_pdf.file_path):
                os.remove(old_pdf.file_path)
            old_pdf.delete()

        # Generate new PDF
        pdf_path = generate_medical_report(analysis)

        # Save new PDF record
        PDFReport.objects.create(
            analysis=analysis,
            file_path=pdf_path,
            file_size=os.path.getsize(pdf_path)
        )

        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="medical_report_{analysis.id}.pdf"'
            return response

    except Exception as e:
        messages.error(request, f'PDF generation failed: {str(e)}')
        return redirect('analysis_results', analysis_id=analysis_id)



@csrf_exempt
@require_http_methods(["POST"])
def upload_and_analyze_api(request):
    """API endpoint for mobile/external integrations"""
    try:
        # Handle file upload and analysis
        # Implementation depends on your API requirements
        pass
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)