from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2
import cvzone
import math
import os

class ObjectDetection():
    def __init__(self, capture):
        self.capture = capture
        self.model = self.load_model()
        self.CLASS_NAMES_DICT = self.model.model.names

    def load_model(self):
        model = YOLO("yolov8n.pt")
        model.fuse()
        return model

    def predict(self, img):
        results = self.model.predict(img, classes=[1, 2, 3, 5, 7], stream=True)
        return results

    def plot_boxes(self, results, img):
        detections = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1,y1,x2,y2 = box.xyxy[0]
                x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
                w,h = x2-x1, y2-y1

                cls = int(box.cls[0])
                currentClass = self.CLASS_NAMES_DICT[cls]

                conf = math.ceil(box.conf[0]*100)/100

                if conf > 0.5:
                    detections.append((([x1, y1, w, h]), conf, currentClass))

        return detections, img

    def track_detect(self, detections, img, tracker):
        tracks = tracker.update_tracks(detections, frame=img)

        for track in tracks:
            if not track.is_confirmed():
                continue
            ltrb = track.to_ltrb()

            bbox = ltrb

            x1,y1,x2,y2 = bbox
            x1,y1,x2,y2 = int(x1), int(y1), int(x2), int(y2)
            w,h = x2-x1, y2-y1

            cvzone.cornerRect(img, (x1,y1,w,h), l=9, rt=1, colorR=(255,0,255))

            x_center = img.shape[1] / 2
            y_center = img.shape[0] / 2

            direction = math.atan2(y1 - y_center, x1 - x_center)

    
            traffic_direction = math.atan2(y_center - 0.5, x_center - 0.5)

  
            if abs(direction - traffic_direction) < math.pi / 2:
                img_wrong_way = img[y1:y1 + h, x1:x1 + w]

                if not os.path.exists("hasil"):
                    os.mkdir("hasil")

                nama_file = f"hasil/{track.track_id}.jpg"

                if not os.path.exists(nama_file):
                    cv2.imwrite(nama_file, img_wrong_way)

                cvzone.putTextRect(img, "Salah Arah", (x1, y1), scale=1, thickness=1, colorR=(0, 0, 255))
                    
            else:
                cvzone.putTextRect(img, f'ID: {track.track_id}', (x1,y1), scale=1, thickness=1, colorR=(0, 255, 0))


        return img

    def __call__(self):
        cap = cv2.VideoCapture(self.capture)
        assert cap.isOpened()
        tracker = DeepSort(max_age=15,
                n_init=5,
                nms_max_overlap=1.0,
                max_cosine_distance=0.7,
                nn_budget=None,
                override_track_class=None,
                embedder="mobilenet",
                half=True,
                bgr=True,
                embedder_gpu=True,
                embedder_model_name=None,
                embedder_wts=None,
                polygon=False,
                today=None)

        while True:
            _, img = cap.read()
            assert _

            results = self.predict(img)
            detections, frames = self.plot_boxes(results, img)
            detect_frame = self.track_detect(detections, frames, tracker)

            cv2.imshow('Image', detect_frame)
            if cv2.waitKey(1) == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()



detector = ObjectDetection(capture='video9.mp4')
detector()