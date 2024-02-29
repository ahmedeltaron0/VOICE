from flask import Flask, render_template, request, url_for,send_from_directory,jsonify
from moviepy.editor import *
import os
from werkzeug.utils import secure_filename
from codes.video_input import video
from codes.transcription import transcribe_audio
from codes.translation import translate_text
from codes.cloning import generate_speech
from codes.audio_process import convert_audio_to_wav
from codes.text_input import test_translation_and_speech_generation

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), UPLOAD_FOLDER)
app.config['OUTPUT_FOLDER'] = os.path.join(os.getcwd(), OUTPUT_FOLDER, 'text')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video/', methods=['GET', 'POST'])
def process():
    video_url = audio_url = output_audio_url = None

    if request.method == 'POST':
        # Check for video file in the uploaded files
        video_file = request.files.get('video_file')
        if video_file and video_file.filename:
            video_file_path = os.path.join(app.config['UPLOAD_FOLDER'], video_file.filename)
            video_file.save(video_file_path)
            video_url = url_for('uploaded_file', filename=video_file.filename)
        
        # Handle optional audio file upload
        audio_file = request.files.get('audio_file')
        if audio_file and audio_file.filename:
            audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_file.filename)
            audio_file.save(audio_file_path)
            audio_url = url_for('uploaded_file', filename=audio_file.filename)
        
        target_language = request.form.get('target_language')
        
        # Call your processing pipeline with the video and optional audio file
        # Assume the result is the path to the processed output audio
        # For demonstration, using audio_file_path as the processed result
        output_audio_path = video(video_file_path, target_language, audio_file_path)
        if output_audio_path:
            output_audio_url = url_for('uploaded_file', filename=os.path.basename(output_audio_path))
        
        return render_template('video.html', video_url=video_url, audio_url=audio_url, output_audio_url=output_audio_url)

    return render_template('video.html')

# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/audio/', methods=['GET', 'POST'])
def process_audio():
    if request.method == 'POST':
        # Handle main audio file upload
        audio_file = request.files.get('audio_file')
        # Handle clone audio file upload
        clone_audio_file = request.files.get('clone_audio_file')
        target_lang = request.form.get('target_language')
        
        if audio_file and clone_audio_file and target_lang:
            # Secure the filenames and save the files
            audio_filename = secure_filename(audio_file.filename)
            audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], audio_filename)
            audio_file.save(audio_file_path)
            
            clone_audio_filename = secure_filename(clone_audio_file.filename)
            clone_audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], clone_audio_filename)
            clone_audio_file.save(clone_audio_file_path)
            
            # Begin the processing pipeline
            wav_audio_path = convert_audio_to_wav(audio_file_path)
            if wav_audio_path:
                transcribed_text = transcribe_audio(wav_audio_path)
                if transcribed_text:
                    translated_text = translate_text(transcribed_text, target_lang)
                    if translated_text:
                        # Pass the translated text and clone audio file path to generate speech
                        output_audio_path = generate_speech(target_lang, translated_text, clone_audio_file_path)
                        if output_audio_path:
                            output_audio_url = url_for('static', filename=os.path.basename(output_audio_path), _external=True)
                            return render_template('audio.html', output_audio_url=output_audio_url)
            
            # Handle failures in the pipeline
            return render_template('error.html', message="Processing failed at some stage.")
        
        # Handle missing files or target language
        return render_template('error.html', message="Missing required files or target language.")
    
    # GET request: just render the form
    return render_template('audio.html')

@app.route('/check_audio_status')
def check_audio_status():
    if 'output_audio_url' in globals():
        return jsonify({"is_processed": True, "audio_url": output_audio_url})
    else:
        return jsonify({"is_processed": False})

@app.route('/text', methods=['GET', 'POST'])
def translate_and_generate_speech():
    if request.method == 'POST':
        # Get form data
        text_to_translate = request.form['text_to_translate']
        target_language = request.form['target_language']
        
        # Handle clone audio file upload
        clone_audio_file = request.files['clone_audio_file']
        if clone_audio_file:
            filename = secure_filename(clone_audio_file.filename)
            clone_audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            clone_audio_file.save(clone_audio_path)
            
            # Proceed with translation and speech generation
            output_audio_path = test_translation_and_speech_generation(text_to_translate, target_language, clone_audio_path)
            if output_audio_path:
                # Redirect to a new URL or render a template with the result
                return render_template('text.html', audio_path=output_audio_path)
            else:
                return "An error occurred during processing."
        else:
            return "No clone audio file provided."
    
    # If not POST, render the submission form
    return render_template('text.html')
if __name__ == '__main__':
    app.run(debug=True)
