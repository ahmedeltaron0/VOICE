from moviepy.editor import *
import os

def convert_video_to_audio_and_split(local_video_path):
    output_directory = r'E:\VOICE\uploads'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        
    audio_path = os.path.join(output_directory, os.path.splitext(os.path.basename(local_video_path))[0] + '.wav')
    try:
        video = VideoFileClip(local_video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        video.close()
        audio.close()
        print("Video was successfully converted to audio")
        return audio_path  
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return None
