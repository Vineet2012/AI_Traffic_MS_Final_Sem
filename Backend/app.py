import os

from algo import optimize_traffic
from detect import detect_cars
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Ensure upload directory exists
if not os.path.exists('uploads'):
    os.makedirs('uploads')

@app.route('/')
def home():
    return "🚦 AI Traffic Optimizer is live."

@app.route('/ping')
def ping():
    return "pong"

@app.route('/upload', methods=['POST'])
def upload_files():
    if 'videos' not in request.files or len(request.files.getlist('videos')) != 4:
        return jsonify({"error": "Please upload exactly 4 videos."}), 400

    video_files = request.files.getlist('videos')
    directions = ['north', 'south', 'west', 'east']
    video_paths = []

    try:
        # Save uploaded videos with directional names
        for i, video in enumerate(video_files):
            if not video.filename.endswith(('.mp4', '.avi', '.mov')):
                return jsonify({"error": "Only MP4, AVI, and MOV formats are allowed."}), 400

            path = f"uploads/{directions[i]}.mp4"
            video.save(path)
            video_paths.append(path)

        # Collect traffic data per video
        traffic_data = []
        for i, video_path in enumerate(video_paths):
            detection = detect_cars(video_path)
            if detection is None:
                return jsonify({"error": f"Error processing video: {video_path}"}), 500

            traffic_data.append({
                'direction': directions[i],
                'vehicle_count': detection['vehicle_count'],
                'ambulance_detected': detection['ambulance_detected'],
                'ambulance_lanes': detection.get('ambulance_lanes', []),
                'mean_peak_value': detection.get('mean_peak_value', 0)
            })

        # Optimize traffic using the structured detection data
        signal_durations = optimize_traffic(traffic_data)
        if not signal_durations or not isinstance(signal_durations, dict):
            return jsonify({"error": "Traffic optimization failed."}), 500

        return jsonify(signal_durations)

    except Exception as e:
        print(f"Exception: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500



if __name__ == '__main__':
    if not os.path.isdir('uploads'):
        os.mkdir('uploads')
    app.run(debug=True)
