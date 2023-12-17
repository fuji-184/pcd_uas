from ultralytics import YOLO

model = YOLO('yolov8n.pt')

results = model.track(source="video5.mp4", show=True, tracker="bytetrack.yaml")  # Tracking with default tracker
#results = model.track(source="https://youtu.be/LNwODJXcvt4", show=True, tracker="bytetrack.yaml")  # Tracking with ByteTrack tracker