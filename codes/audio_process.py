import os
from moviepy.editor import *


def convert_audio_to_wav(audio_file_path):
    while True:
        # Prompt the user to enter the path to the audio file
        audio_file_path = audio_file_path
        
        # Ensure the provided file path is valid
        if not os.path.exists(audio_file_path):
            print("Error: The specified audio file does not exist. Please try again.")
        else:
            break  # Exit the loop if a valid file path is provided
    
    # Ensure the output directory exists
    output_directory = r'E:\Integration_2024\uploads'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    
    # Construct the output audio file path
    output_audio_path = os.path.join(output_directory, os.path.splitext(os.path.basename(audio_file_path))[0] + '.wav')
    
    try:
        # Load the audio file
        audio = AudioFileClip(audio_file_path)
        
        # Write the audio to a WAV file
        audio.write_audiofile(output_audio_path)
        
        # Close the audio object to free resources
        audio.close()
        
        print("Audio was successfully converted to WAV format")
        return output_audio_path  # Return the output audio path
    
    except Exception as e:
        print(f"An error occurred during conversion: {e}")
        return None
def main():
    # Call the function to convert audio to WAV format
    converted_audio_path = convert_audio_to_wav()
    
    if converted_audio_path:
        print(f"Converted audio file saved at: {converted_audio_path}")
    else:
        print("Failed to convert audio file.")

if __name__ == "__main__":
    main()