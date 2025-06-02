# Darwix AI - Blog Platform with AI Features

This Django-based blog platform includes two main AI features:
1. Audio Transcription with Speaker Diarization
2. AI-powered Blog Post Title Suggestions

## Setup Instructions for Windows

1. Install FFmpeg:
   - Download FFmpeg from https://ffmpeg.org/download.html
   - Extract the downloaded zip file
   - Add the `bin` folder to your system's PATH environment variable
   - Verify installation by opening Command Prompt and typing: `ffmpeg -version`

2. Create a virtual environment:
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. Install dependencies:
```powershell
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
HUGGINGFACE_TOKEN=your_token_here
```

5. Run migrations:
```powershell
python manage.py migrate
```

6. Start the development server:
```powershell
python manage.py runserver
```

## API Endpoints

### Audio Transcription
- Endpoint: `/api/transcribe/`
- Method: POST
- Input: Audio file (WAV, MP3)
- Output: JSON with transcription and speaker diarization

### Title Suggestions
- Endpoint: `/api/suggest-titles/`
- Method: POST
- Input: Blog post content
- Output: JSON with 3 title suggestions

## Testing the Features

1. Audio Transcription (using PowerShell):
```powershell
$filePath = "path\to\your\audio.wav"
$uri = "http://localhost:8000/api/transcribe/"
$form = @{
    audio_file = Get-Item -Path $filePath
    language = "en"  # optional
    task = "transcribe"  # optional
}
Invoke-RestMethod -Uri $uri -Method Post -Form $form
```
![WhatsApp Image 2025-06-03 at 02 27 46_28901752](https://github.com/user-attachments/assets/ba77c399-f2c1-4cf5-b507-3afb38275f73)
![WhatsApp Image 2025-06-03 at 02 28 02_446c9f19](https://github.com/user-attachments/assets/ec18f20a-ea69-4688-a08a-2d4b73649c07)


2. Title Suggestions (using PowerShell):
```powershell
$uri = "http://localhost:8000/api/suggest-titles/"
$body = @{
    content = "Your blog post content here"
} | ConvertTo-Json
Invoke-RestMethod -Uri $uri -Method Post -Body $body -ContentType "application/json"
```

## Troubleshooting

1. If you get a "ffmpeg not found" error:
   - Make sure FFmpeg is properly installed
   - Verify FFmpeg is in your system PATH
   - Restart your terminal after adding FFmpeg to PATH

2. If you get CUDA-related errors:
   - Make sure you have NVIDIA GPU drivers installed
   - Install CUDA Toolkit if you want to use GPU acceleration
   - Or force CPU usage by setting device="cpu" in TranscriptionService initialization

3. If you get memory errors:
   - Try using a smaller Whisper model (e.g., "tiny" or "base" instead of "large")
   - Close other memory-intensive applications
   - Process shorter audio files
