import whisper
from pyannote.audio import Pipeline
import torch
import json
import os
from typing import Dict, List, Optional
from pathlib import Path

class TranscriptionService:
    def __init__(self, model_size: str = "base", device: Optional[str] = None):
        """
        Initialize the transcription service.
        
        Args:
            model_size (str): Size of the Whisper model to use. Options: "tiny", "base", "small", "medium", "large"
            device (str): Device to run the model on ("cuda", "cpu", or None for auto)
        """
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.device = device
        self.whisper_model = whisper.load_model(model_size, device=device)
        self.diarization_pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization",
            use_auth_token=os.getenv("HUGGINGFACE_TOKEN")
        )

    def transcribe_with_diarization(
        self, 
        audio_path: str,
        language: Optional[str] = None,
        task: str = "transcribe"
    ) -> Dict:
        """
        Transcribe audio with speaker diarization.
        
        Args:
            audio_path (str): Path to the audio file
            language (str, optional): Language code (e.g., "en", "es", "fr")
            task (str): Either "transcribe" or "translate"
            
        Returns:
            Dict containing transcription segments with speaker information
        """
        # Convert path to absolute path and handle Windows paths
        audio_path = str(Path(audio_path).resolve())
        
        # Verify file exists
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
            
        # Transcribe audio with Whisper
        result = self.whisper_model.transcribe(
            audio_path,
            language=language,
            task=task,
            verbose=False
        )
        
        # Perform diarization
        diarization = self.diarization_pipeline(audio_path)
        
        # Combine transcription with diarization
        segments = []
        for segment in result["segments"]:
            speaker = self._get_speaker_for_segment(segment, diarization)
            segments.append({
                "start": segment["start"],
                "end": segment["end"],
                "speaker": speaker,
                "text": segment["text"],
                "confidence": segment.get("confidence", None)
            })
        
        return {
            "segments": segments,
            "full_text": result["text"],
            "language": result.get("language", language),
            "task": task
        }

    def _get_speaker_for_segment(self, segment: Dict, diarization) -> str:
        # Find the most likely speaker for this segment
        start_time = segment["start"]
        end_time = segment["end"]
        
        # Get speaker for the middle of the segment
        mid_time = (start_time + end_time) / 2
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            if turn.start <= mid_time <= turn.end:
                return f"Speaker_{speaker.split('_')[-1]}"
        
        return "Unknown" 