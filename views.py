from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import os
from pathlib import Path
from .services.transcription_service import TranscriptionService
from .services.title_suggestion_service import TitleSuggestionService
from .models import BlogPost

# Initialize services with default settings
transcription_service = TranscriptionService(model_size="base")  # You can change model size here
title_suggestion_service = TitleSuggestionService()

@csrf_exempt
@require_http_methods(["POST"])
def transcribe_audio(request):
    if 'audio_file' not in request.FILES:
        return JsonResponse({'error': 'No audio file provided'}, status=400)
    
    audio_file = request.FILES['audio_file']
    
    # Get optional parameters
    language = request.POST.get('language', None)
    task = request.POST.get('task', 'transcribe')
    
    # Validate task parameter
    if task not in ['transcribe', 'translate']:
        return JsonResponse({'error': 'Invalid task parameter. Must be either "transcribe" or "translate"'}, status=400)
    
    # Create temp directory if it doesn't exist
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    
    # Save the file temporarily with a unique name
    temp_path = temp_dir / f"temp_{audio_file.name}"
    with open(temp_path, 'wb+') as destination:
        for chunk in audio_file.chunks():
            destination.write(chunk)
    
    try:
        # Process the audio file
        result = transcription_service.transcribe_with_diarization(
            str(temp_path),
            language=language,
            task=task
        )
        
        # Clean up
        temp_path.unlink(missing_ok=True)
        
        return JsonResponse(result)
    except Exception as e:
        # Clean up in case of error
        temp_path.unlink(missing_ok=True)
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def suggest_titles(request):
    try:
        data = json.loads(request.body)
        content = data.get('content')
        
        if not content:
            return JsonResponse({'error': 'No content provided'}, status=400)
        
        # Generate title suggestions
        suggestions = title_suggestion_service.generate_title_suggestions(content)
        
        return JsonResponse({
            'suggestions': suggestions
        })
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500) 