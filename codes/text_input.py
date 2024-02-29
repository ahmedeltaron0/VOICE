from codes.translation import translate_text
from codes.cloning import generate_speech, check_lang  # Assuming this function checks/modifies the language code for speech generation

def test_translation_and_speech_generation(text_to_translate, target_language, clone_audio_path):
    # Translate the text
    translated_text = translate_text(text_to_translate, target_language)
    if translated_text:
        print("Translated text:", translated_text)
        
        # Generate speech from the translated text
        output_audio_path = generate_speech(check_lang(target_language), translated_text, clone_audio_path)
        if output_audio_path:
            print("Speech generated successfully and saved to:", output_audio_path)
            return output_audio_path
        else:
            print("Error occurred during speech generation.")
    else:
        print("Error occurred during translation.")
