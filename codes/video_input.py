from moviepy.editor import *
from codes.video_process import convert_video_to_audio_and_split
from codes.transcription import transcribe_audio
from codes.translation import translate_text
from codes.cloning import generate_speech, check_lang

# ------> TESTING <------

# Define the test function
def video (video_path, target_language, clone_audio_path):
    # Step 0: Input video file path
    # video_path = input("Enter the path of the video file: ")
    video_path = video_path

    # Step 1: Convert video to audio
    audio_path = convert_video_to_audio_and_split(video_path)
    if audio_path:
        print("Audio file created successfully:", audio_path)
    else:
        print("Error occurred during audio conversion.")
        return

    # Step 2: Transcribe audio to text
    transcribed_text = transcribe_audio(audio_path)
    if transcribed_text:
        print("Transcription successful:", transcribed_text)
    else:
        print("Error occurred during transcription.")
        return

    # Step 3: Input target language
    target_language = target_language

    # Step 4: Translate the transcribed text
    translated_text = translate_text(transcribed_text, target_language)
    if translated_text:
        print("Translation successful:", translated_text)
    else:
        print("Error occurred during translation.")
        return
    
    # Step 5: Prompt user for clone audio file path
    clone_audio_path = clone_audio_path
    
    # Step 6: Generate speech
    output_audio_path = generate_speech(check_lang(target_language), translated_text, clone_audio_path)
    if output_audio_path:
        print("Speech generated successfully and saved to:", output_audio_path)
    else:
        print("Error occurred during speech generation.")
        return

# # Call the test function
# if __name__ == "__main__":
#     test_processing_pipeline()