import time
import cv2
from helpers import annotate_frame
from os import environ
from warn import warn
from threading import Thread

def camera_loop(model, yolo_gui):
        all_detected_classes = set()
        frame_count = 0#Number of frames where eyes are closed
        
        with yolo_gui.camera_state:
            if yolo_gui.camera_paused:
                yolo_gui.camera_state.wait()
            while cv2.VideoCapture(0):
                ret, frame = yolo_gui.cap.read()
                frame_start = time.perf_counter()
                if not ret:
                    break
                frame = cv2.flip(frame, 1)
                yolo_gui.current_frame = frame.copy()
            
                # --- get results and update detected classes --- 
                visible_classes = yolo_gui.get_visible_classes()
                annotated_frame, results = annotate_frame(model, frame, visible_classes)
                yolo_gui.current_results = results
            
                # --- collect all detected classes across frames --- 
                if results and results.boxes:
                    for box in results.boxes:
                        cls_id = int(box.cls[0])
                        class_name = model.names[cls_id]
                        all_detected_classes.add(class_name)
                else:
                    frame_count += 1#increment count if no eyes are detected

                if frame_count > yolo_gui.threashold:
                    yolo_gui.warnings += 1
                    #warn(yolo_gui.warnings)
                    #Thread
                    Thread(target=warn(yolo_gui.warnings), daemon=False).run()
                    yolo_gui.frames = 0
                    frame_count = 0
            
                if yolo_gui.frames == yolo_gui.time_limit:
                    yolo_gui.frames = 0
                    frame_count = 0
                    """Program only checks for amount of time with
                    eyes closed per 5 seconds.
                    Therefore frame_count resets every 150 frames (30fps)"""
            
                # ---  update checkboxes if new classes detected --- 
                current_checkbox_classes = set(yolo_gui.class_vars.keys())
                if all_detected_classes != current_checkbox_classes:
                    # Preserve current checkbox states
                    current_states = {name: var.get() for name, var in list(yolo_gui.class_vars.items())}
                    yolo_gui.update_class_checkboxes(all_detected_classes)
                    # --- restore previous states, new classes default to True --- 
                    for name, var in list(yolo_gui.class_vars.items()):
                        if name in current_states:
                            var.set(current_states[name])
            
                yolo_gui.display_image(annotated_frame)
                yolo_gui.display_detections(results)
                delta_time = time.perf_counter() - frame_start
                sleep_time = yolo_gui.frame_duration - delta_time

                yolo_gui.threashold = 1 / yolo_gui.frame_duration
        
                if sleep_time > 0 and yolo_gui.limit_fps:
                    time.sleep(sleep_time)
                print("Frame count is: ", frame_count)
            
                if yolo_gui.set_limit == False:
                    yolo_gui.time_limit = yolo_gui.threashold * 5
                    print("Threashold set at " + str(yolo_gui.time_limit) + " frames.")
                    print("We are running at " + str(yolo_gui.threashold) + " fps.")

                    yolo_gui.set_limit = True

                yolo_gui.frames += 1

            environ["OPENCV_LOG_LEVEL"] = "SILENT"

            yolo_gui.stop_camera()