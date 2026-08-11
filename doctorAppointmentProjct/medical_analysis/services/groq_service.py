import base64
import json
import logging
import os

from groq import Groq
from django.conf import settings
from typing import Dict, List, Optional
import traceback

logger = logging.getLogger(__name__)


class GroqMedicalService:
    def __init__(self):
        try:
            self.api_key = getattr(settings, 'GROQ_API_KEY', None)
            if not self.api_key:
                raise ValueError("GROQ_API_KEY not found in settings")

            self.client = Groq(api_key=self.api_key)

            # Use available models - check Groq documentation for current models
            self.text_model = "llama-3.3-70b-versatile"  # Fast model for text
            self.vision_model = "meta-llama/llama-4-scout-17b-16e-instruct"  # Vision model

            print(f"GroqMedicalService initialized with API key: {self.api_key[:10]}...")

        except Exception as e:
            logger.error(f"Failed to initialize GroqMedicalService: {str(e)}")
            raise

    def test_connection(self):
        """Test the API connection"""
        try:
            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=10
            )
            return True, "Connection successful"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"


    def analyze_medical_image(self, image_path: str, symptoms: str = "") -> Dict:
        """Analyze medical images using Groq's vision model"""
        try:
            print(f"Starting image analysis for: {image_path}")

            # Check if file exists
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image file not found: {image_path}")

            # Convert image to base64
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')

            print(f"Image encoded, size: {len(base64_image)} characters")

            prompt = f"""
            Analyze this medical image and provide a JSON response with:
            1. Visual observations
            2. Possible conditions with confidence levels
            3. Severity assessment
            4. Recommendations

            Additional context: {symptoms if symptoms else 'No additional symptoms provided'}

            Respond ONLY with valid JSON in this format:
            {{
                "visual_observations": ["Clear visual observation 1", "Clear visual observation 2"],
                "possible_conditions": [
                    {{"condition": "Condition Name", "confidence": "80%", "reasoning": "Why this condition fits"}}
                ],
                "severity_assessment": "low",
                "recommendations": ["Recommendation 1", "Recommendation 2"],
                "warning_signs": ["Sign to watch for"],
                "next_steps": ["Step 1", "Step 2"],
                "disclaimer": "This analysis is for informational purposes only."
            }}
            """

            response = self.client.chat.completions.create(
                model=self.vision_model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.2,
                max_tokens=1500
            )

            result_text = response.choices[0].message.content.strip()
            print(f"Image analysis response: {result_text}")

            # Parse JSON response
            try:
                if result_text.startswith('```json'):
                    result_text = result_text.replace('```json', '').replace('```', '')
                elif result_text.startswith('```'):
                    result_text = result_text.replace('```', '')

                result_json = json.loads(result_text.strip())
                return result_json

            except json.JSONDecodeError:
                return {
                    "visual_observations": ["Image processed but analysis format error"],
                    "possible_conditions": [
                        {"condition": "Analysis Error", "confidence": "N/A", "reasoning": "Could not parse response"}
                    ],
                    "severity_assessment": "unknown",
                    "recommendations": ["Please try again with a different image"],
                    "warning_signs": ["Contact healthcare provider if symptoms worsen"],
                    "next_steps": ["Retry analysis", "Consult medical professional"],
                    "disclaimer": "Analysis could not be completed properly.",
                    "error": "JSON parsing failed",
                    "raw_response": result_text[:500]
                }

        except Exception as e:
            logger.error(f"Error in image analysis: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            return {
                "error": "Image analysis failed",
                "message": f"Error: {str(e)}",
                "visual_observations": ["Could not process image"],
                "possible_conditions": [
                    {"condition": "Analysis Failed", "confidence": "N/A", "reasoning": "Technical error occurred"}
                ],
                "recommendations": ["Please try again", "Ensure image is clear and properly formatted"],
                "disclaimer": "Image analysis could not be completed due to technical issues."
            }

    def get_ai_assistant_response(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Generate AI assistant responses for user guidance"""
        try:
            print(f"AI Assistant query: {user_message}")

            system_prompt = """
            You are a helpful medical AI assistant for a medical analysis platform. 

            Your role is to:
            1. Help users understand how to use the platform
            2. Provide general health information
            3. Guide users on when to seek professional medical help
            4. Answer questions about symptoms and health concerns
            5. Explain medical analysis features

            Always be empathetic, clear, and emphasize the importance of professional medical consultation for serious concerns.
            Keep responses helpful but concise (2-3 paragraphs maximum).

            IMPORTANT: Never provide specific medical diagnoses. Always recommend consulting healthcare providers for medical issues.
            """

            messages = [{"role": "system", "content": system_prompt}]

            # Add conversation history if provided (last 5 messages for context)
            if conversation_history:
                messages.extend(conversation_history[-5:])

            messages.append({"role": "user", "content": user_message})

            response = self.client.chat.completions.create(
                model=self.text_model,
                messages=messages,
                temperature=0.7,
                max_tokens=800
            )

            ai_response = response.choices[0].message.content.strip()
            print(f"AI Assistant response: {ai_response[:100]}...")
            return ai_response

        except Exception as e:
            logger.error(f"Error in AI assistant response: {str(e)}")
            logger.error(f"Traceback: {traceback.format_exc()}")

            return f"I'm sorry, I'm having trouble responding right now. Error: {str(e)}. Please try again in a moment."


# Initialize service instance
try:
    groq_service = GroqMedicalService()
    print("Groq service initialized successfully")
except Exception as e:
    print(f"Failed to initialize Groq service: {str(e)}")
    groq_service = None