from faster_whisper import WhisperModel

def transcribe_audio(audio_path):
    model = WhisperModel("large-v3", compute_type="float32", device="cpu")
    segments, _ = model.transcribe(audio_path)
    transcriptions = ""
    for segment in segments:
        transcriptions += segment.text + " "    
    return transcriptions.strip()
