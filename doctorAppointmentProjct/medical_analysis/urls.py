from django.urls import path
from . import views

urlpatterns = [

    path('analyze/image/', views.image_analysis_view, name='image_analysis'),

    path('results/<uuid:analysis_id>/', views.analysis_results, name='analysis_results'),
    path('assistant/', views.ai_assistant_chat, name='ai_assistant_chat'),
    path('assistant/<uuid:session_id>/', views.ai_assistant_chat, name='ai_assistant_chat'),
    path('report/<uuid:analysis_id>/pdf/', views.generate_pdf_report, name='generate_pdf_report'),
    path('api/upload-analyze/', views.upload_and_analyze_api, name='upload_analyze_api'),
]