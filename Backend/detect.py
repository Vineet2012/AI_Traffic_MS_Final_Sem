import os
import time
from collections import deque

import cv2 as cv
import numpy as np
from scipy.signal import find_peaks
from ultralytics import YOLO


def detect_cars(video_file):
    # Green color for general vehicles
    COLOR_VEHICLE = (0, 255, 0)

    # Load YOLOv8 model
    model_path = os.path.join('Models', 'best.pt')
    model = YOLO(model_path)

    print("Model classes:", model.names)

    cap = cv.VideoCapture(video_file)
    frame_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    starting_time = time.time()
    frame_counter = 0

    num_lanes = 3  # Adjust as needed
    lane_width = frame_width // num_lanes

    # Define lane directions (1-indexed)
    lane_directions = {
        1: "Westbound",
        2: "Northbound",
        3: "Eastbound"
    }

    # Create display window
    cv.namedWindow('frame', cv.WINDOW_NORMAL)
    cv.resizeWindow('frame', 960, 540)
    cv.moveWindow('frame', 480, 270)

    car_counts = deque()  # (timestamp, count)
    ambulance_directions = []  # store detected directions of ambulances

    vehicle_classes = ["Ambulance", "Bus", "Car", "Motorcycle", "Truck"]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_counter += 1

        # YOLO prediction
        results = model.predict(frame, conf=0.3, verbose=False)[0]

        car_count = 0
        for box in results.boxes:
            class_id = int(box.cls.item())
            confidence = float(box.conf.item())
            label = model.names[class_id]

            if label in vehicle_classes:
                coords = box.xyxy[0].cpu().numpy().astype(int)
                x1, y1, x2, y2 = coords
                center_x = (x1 + x2) // 2

                # Determine lane (1-indexed)
                lane_idx = center_x // lane_width + 1
                lane_direction = lane_directions.get(lane_idx, "Unknown")

                if label == "Ambulance":
                    color = (0, 0, 255)  # Red
                    print(f"Ambulance detected in lane {lane_idx} ({lane_direction})")
                    label_text = f'{label} ({lane_direction})'
                    ambulance_directions.append(lane_direction)
                else:
                    color = COLOR_VEHICLE
                    label_text = f'{label}: {confidence:.2f}'

                # Draw bounding box and label
                cv.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                cv.putText(frame, label_text, (x1, y1 - 10),
                           cv.FONT_HERSHEY_COMPLEX, 0.5, color, 2)

                car_count += 1

        current_time = time.time()
        car_counts.append((current_time, car_count))

        # Keep last 30 seconds of data
        while car_counts and car_counts[0][0] < current_time - 30:
            car_counts.popleft()

        # Analyze peaks
        car_count_values = [count for _, count in car_counts]
        peaks, _ = find_peaks(car_count_values)
        mean_peak_value = np.mean([car_count_values[i] for i in peaks]) if peaks.size > 0 else (
            np.mean(car_count_values) if car_count_values else 0)

        # FPS calculation
        ending_time = time.time()
        fps = frame_counter / (ending_time - starting_time)
        cv.putText(frame, f'FPS: {fps:.2f}', (20, 50),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)

        # Show mean peak
        cv.putText(frame, f'Mean Peak Vehicles: {mean_peak_value:.2f}', (20, 80),
                   cv.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 255), 2)

        # Display the frame
        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv.destroyAllWindows()

    print("\nDetected Ambulance Directions:")
    for direction in ambulance_directions:
        print(f"- {direction}")

    return {
        'vehicle_count': mean_peak_value,
        'ambulance_detected': len(ambulance_directions) > 0,
        'ambulance_lanes': ambulance_directions
    }
