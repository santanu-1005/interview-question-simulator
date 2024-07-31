from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import random
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Directory to store videos locally
LOCAL_STORAGE_DIR = 'local_storage'
os.makedirs(LOCAL_STORAGE_DIR, exist_ok=True)

# Load questions from text file or list
questions = [
    "Tell Us something about Yourself?",
    "Why are you interested in this internship, and how does it align with your career goals?",
    "What specific skills or knowledge do you hope to gain from this internship?",
    "Can you provide an example of a time when you had to work as part of a team? What was your approach to collaboration, and how did you handle any conflicts or challenges?",
    "Can you describe a project or task from your previous experience (or academic work) that you are particularly proud of? What was your role, and what did you learn from it?",
    "Describe a situation where you had to quickly learn something new or adapt to a change. How did you handle it, and what was the outcome?",
    "What motivated you to apply for this internship, and what interests you about our company or the role?",
    "What skills or strengths do you believe you bring to this internship, and how do you think they will help you succeed?",
    "How do you handle challenges or setbacks, especially when you are working on something unfamiliar or difficult?",
    "Can you tell us about your educational background and any relevant coursework or projects you have completed?",
    "What are your strengths and weaknesses, and how do you plan to address your weaknesses during this internship?",
    "How do you handle feedback and criticism, and can you give an example of how you have used feedback to improve your work?",
    "How would you approach a project or task if you were unfamiliar with the topic or required specific knowledge?",
    "What tools or software are you familiar with that are relevant to this internship role?",
    "What are your long-term career goals, and how does this internship help you achieve them?",
    "Can you give an example of a situation where you had to communicate complex information to someone with less expertise?",
    "How would you handle a situation where you were given unclear instructions or expectations for a task?",
    "What extracurricular activities or volunteer experiences have you been involved in, and how do they relate to this internship?",
    "How do you plan to balance this internship with any other commitments you may have?"
]

# Route to start the interview
@app.route('/', methods=['GET'])
def start_interview():
    return render_template('temp.html')

# Route to check mic and camera
@app.route('/check-devices', methods=['POST'])
def check_devices():
    mic_working = check_mic()
    camera_working = check_camera()
    return jsonify({
        'status': 'success' if mic_working and camera_working else 'error',
        'mic': mic_working,
        'camera': camera_working
    }), 200

# Route to conduct interview
@app.route('/conduct-interview', methods=['POST'])
def conduct_interview():
    # Ensure the sample size does not exceed the number of available questions
    num_questions = 6
    if len(questions) < num_questions:
        selected_questions = questions  # Use all available questions
    else:
        selected_questions = random.sample(questions, num_questions)
    
    return jsonify({'questions': selected_questions})

# Route to save video
@app.route('/save-video', methods=['POST'])
def save_video():
    if 'video' not in request.files:
        return jsonify({'status': 'error', 'message': 'No video file provided'}), 400
    
    video_data = request.files['video']
    if video_data.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"interview_{timestamp}.mp4"
    local_video_path = os.path.join(LOCAL_STORAGE_DIR, video_filename)
    
    try:
        # Save video locally
        video_data.save(local_video_path)
        
        # Uncomment if you have S3 setup
        # s3.upload_file(local_video_path, BUCKET_NAME, video_filename)
        
        # Remove local video file after upload if using S3
        # os.remove(local_video_path)
        
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error saving video: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to save video'}), 500

# Route to save audio (if needed)
@app.route('/save-audio', methods=['POST'])
def save_audio():
    if 'audio' not in request.files:
        return jsonify({'status': 'error', 'message': 'No audio file provided'}), 400
    
    audio_data = request.files['audio']
    if audio_data.filename == '':
        return jsonify({'status': 'error', 'message': 'No selected file'}), 400
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_filename = f"interview_{timestamp}.wav"
    local_audio_path = os.path.join(LOCAL_STORAGE_DIR, audio_filename)
    
    try:
        # Save audio locally
        audio_data.save(local_audio_path)
        
        # Uncomment if you have S3 setup
        # s3.upload_file(local_audio_path, BUCKET_NAME, audio_filename)
        
        # Remove local audio file after upload if using S3
        # os.remove(local_audio_path)
        
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        print(f"Error saving audio: {e}")
        return jsonify({'status': 'error', 'message': 'Failed to save audio'}), 500

def check_mic():
    # Placeholder function to simulate mic check
    return True

def check_camera():
    # Placeholder function to simulate camera check
    return True

if __name__ == '__main__':
    app.run(debug=True)
