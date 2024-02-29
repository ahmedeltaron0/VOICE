from moviepy.editor import *
from transcription import transcribe_audio
from translation import translate_text
from cloning import generate_speech
from audio_process import convert_audio_to_wav
#------> TESTING <------
def test_audio_processing(input_audio_path, clone_audio_path, target_lang):
    # Prompt the user for input audio file path
    input_audio_path = input("Enter the path to the input audio file: ")

    # Prompt the user for clone audio file path
    clone_audio_path = input("Enter the path to the clone audio file: ")
    
    # Prompt the user for target language
    target_lang = input("Enter the target language (e.g., 'ar' for Arabic): ")
    
    # Step 1: Convert audio file to WAV
    wav_audio_path = convert_audio_to_wav(input_audio_path)
    
    if wav_audio_path:
        # Step 2: Transcribe audio to text
        transcribed_text = transcribe_audio(wav_audio_path)
        
        if transcribed_text:
            # Step 3: Translate transcribed text
            translated_text = translate_text(transcribed_text, target_lang)
            
            if translated_text:
                # Step 4: Generate speech from translated text
                output_audio_path = generate_speech(target_lang, translated_text, clone_audio_path)
                print("Output audio file:", output_audio_path)
            else:
                print("Translation failed.")
        else:
            print("Transcription failed.")
    else:
        print("Audio conversion failed.")

# Test the audio processing function
test_audio_processing()