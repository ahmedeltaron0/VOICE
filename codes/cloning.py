import os
from TTS.api import TTS
import torch
from pydub import AudioSegment
import time

device = "cuda" if torch.cuda.is_available() else "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

#split text into chunks

def split_text(input_text):
    
    chunk_size = 160
    chunks = []
    current_chunk = ""

    for word in input_text.split():
        if len(current_chunk) + len(word) <= chunk_size:
            current_chunk += word + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = word + " "

    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

#check language

def check_lang(input_lang='arabic'):
    language = {"english": 'en',"spanish": 'es', "french": 'fr',"german": 'de',"italian": 'it',"portuguese": 'pt',"polish": 'pl',"turkish": 'tr',"russian": "ru","dutch": "nl","czech": "cs","arabic": 'ar',"chinese": 'cn',"japanese": "ja","hungarian": 'hu',"korean": 'ko',"hindi": 'hi'}
    print(f"Input language: {input_lang}")  # Debug print

    # Attempt to retrieve the language code from the dictionary
    # If input_lang is not found, default to 'en' (English) or any other valid code
    lang_code = language.get(input_lang.lower(), 'en')  # Default to English if not found

    return lang_code

def generate_speech(input_lang, input_text, input_audio):
    start_time = time.time()
    lang = check_lang(input_lang)
    if lang is None:
        raise ValueError(f"Invalid language input: {input_lang}")
    chunks = split_text(input_text)
    output_audio = AudioSegment.empty()
    
    for chunk in chunks:
        tts.tts_to_file(text=chunk,
                        file_path="output_temp.wav",
                        speaker_wav=input_audio,
                        language=lang)
        chunk_audio = AudioSegment.from_wav("output_temp.wav")
        output_audio += chunk_audio
        os.remove("output_temp.wav")
    
    # Export the combined audio
    output_file_path = r"E:\VOICE\generated\output_All_combined.wav"
    output_audio.export(output_file_path, format="wav")
    
    # Calculate execution time
    end_time = time.time()
    execution_time = end_time - start_time
    print("Execution time:", execution_time)
    
    return output_file_path

