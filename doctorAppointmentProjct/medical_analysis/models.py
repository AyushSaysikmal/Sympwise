from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class MedicalAnalysis(models.Model):
    ANALYSIS_TYPES = [
        ('text', 'Text Analysis'),
        ('image', 'Image Analysis'),
        ('mixed', 'Mixed Analysis'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='analyses')
    analysis_type = models.CharField(max_length=10, choices=ANALYSIS_TYPES)
    symptoms_text = models.TextField(blank=True, null=True)
    uploaded_image = models.ImageField(upload_to='medical_images/', blank=True, null=True)
    analysis_result = models.JSONField(default=dict)
    confidence_score = models.FloatField(default=0.0)
    recommendations = models.TextField(blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Analysis {self.id} - {self.user.username}"


class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_sessions',
        null=True,  # Allow null for anonymous users
        blank=True  # Allow blank in forms
    )
    session_name = models.CharField(max_length=200, default="Medical Consultation")
    created_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    # Optional: Add session key for tracking anonymous sessions
    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        help_text="Session key for anonymous users"
    )

    class Meta:
        ordering = ['-created_at']
        # Add index for better performance when querying anonymous sessions
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['session_key']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        if self.user:
            return f"Chat Session - {self.user.username} - {self.created_at}"
        else:
            return f"Anonymous Chat Session - {self.created_at}"

    @property
    def is_anonymous(self):
        """Check if this is an anonymous session"""
        return self.user is None

    @property
    def display_name(self):
        """Get display name for the session"""
        if self.user:
            return f"{self.user.username}"
        else:
            return "Anonymous User"


class ChatMessage(models.Model):
    MESSAGE_TYPES = [
        ('user', 'User Message'),
        ('assistant', 'Assistant Message'),
        ('system', 'System Message'),
    ]

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    message_type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    content = models.TextField()
    metadata = models.JSONField(default=dict)
    timestamp = models.DateTimeField(default=timezone.now)

    # Optional: Track if message was from anonymous user
    is_anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
        indexes = [
            models.Index(fields=['session', 'timestamp']),
            models.Index(fields=['message_type']),
        ]

    def __str__(self):
        return f"{self.message_type.title()} - {self.session} - {self.timestamp}"

    def save(self, *args, **kwargs):
        # Automatically set is_anonymous based on session
        if self.session and self.session.is_anonymous:
            self.is_anonymous = True
        super().save(*args, **kwargs)


class PDFReport(models.Model):
    analysis = models.OneToOneField(MedicalAnalysis, on_delete=models.CASCADE, related_name='pdf_report')
    file_path = models.CharField(max_length=500)
    generated_at = models.DateTimeField(default=timezone.now)
    file_size = models.IntegerField(default=0)

    def __str__(self):
        return f"Report for {self.analysis.id}"