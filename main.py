import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from ultralytics import YOLO
import threading
import time
from warn import warn
import torch
#import numpy as np
#from inference_mp4 import annotate_video

# Load YOLO model
model = YOLO('best.pt')

# Inference + annotation for image path
def annotate_image(image_path, visible_classes=None):
    results = model(image_path)
    if visible_classes is not None:
        # --- get filtered classes --- 
        filtered_result = filter_results(results[0], visible_classes) 
        return filtered_result.plot(), results[0] 
    return results[0].plot(), results[0]  # BGR image and detection result

# Inference + annotation for frame
def annotate_frame(frame, visible_classes=None):
    results = model(frame)
    if visible_classes is not None:
        # --- get filtered classes --- 
        filtered_result = filter_results(results[0], visible_classes)
        return filtered_result.plot(), results[0] 
    return results[0].plot(), results[0]  # BGR image and detection result

def filter_results(result, visible_classes):
    if not result.boxes or not visible_classes:
        # --- empty result  --- 
        filtered_result = result.new()
        return filtered_result
    
    # --- keep track of indices --- 
    keep_indices = []
    for i, box in enumerate(result.boxes):
        cls_id = int(box.cls[0])
        class_name = model.names[cls_id]
        if class_name in visible_classes:
            keep_indices.append(i)
    
    if not keep_indices:
        # --- empty result --- 
        filtered_result = result.new()
        return filtered_result
    
    # --- add new selected classes --- 
    filtered_result = result.new()
    filtered_result.boxes = result.boxes[keep_indices]
    
    return filtered_result

class YOLO_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("YOLOv8 Annotator")
        self.root.geometry("1200x600")

        # Layout frames
        self.left_frame = tk.Frame(root)
        self.left_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        # Canvas for image or webcam stream
        self.canvas = tk.Canvas(self.left_frame, width=700, height=500)
        self.canvas.pack()

        # Buttons
        #self.upload_button = tk.Button(self.left_frame, text="Upload Image", command=self.upload_image)
        #self.upload_button.pack(side=tk.LEFT, padx=5, pady=10)

        #self.upload_video_button = tk.Button(self.left_frame, text="Upload Video", command=self.upload_video)
        #self.upload_video_button.pack(side=tk.LEFT, padx=5, pady=10)

        self.cam_button = tk.Button(self.left_frame, text="Start Camera", command=self.start_camera)
        self.cam_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.left_frame, text="Stop Camera", command=self.stop_camera, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Video playback controls
        self.video_controls_frame = tk.Frame(self.left_frame)
        self.video_controls_frame.pack(pady=5)

        self.play_pause_button = tk.Button(self.video_controls_frame, text="Play/Pause", command=self.toggle_video_playback, state=tk.DISABLED)
        self.play_pause_button.pack(side=tk.LEFT, padx=5)

        self.stop_video_button = tk.Button(self.video_controls_frame, text="Stop Video", command=self.stop_video, state=tk.DISABLED)
        self.stop_video_button.pack(side=tk.LEFT, padx=5)

        # --- Get filters --- 
        self.filter_frame = tk.Frame(self.right_frame)
        self.filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.filter_frame, text="Class Filters", font=("Arial", 12, "bold")).pack()
        
        # --- scrollable for tick boxes (from stack overflow) --- 
        self.checkbox_canvas = tk.Canvas(self.filter_frame, height=150)
        self.checkbox_scrollbar = tk.Scrollbar(self.filter_frame, orient="vertical", command=self.checkbox_canvas.yview)
        self.checkbox_frame = tk.Frame(self.checkbox_canvas)
        
        # ---- also from stack overflow, but works well --- 
        self.checkbox_frame.bind(
            "<Configure>",
            lambda e: self.checkbox_canvas.configure(scrollregion=self.checkbox_canvas.bbox("all")) 
        )
        
        self.checkbox_canvas.create_window((0, 0), window=self.checkbox_frame, anchor="nw")
        self.checkbox_canvas.configure(yscrollcommand=self.checkbox_scrollbar.set)
        
        self.checkbox_canvas.pack(side="left", fill="both", expand=True)
        self.checkbox_scrollbar.pack(side="right", fill="y")

        # --- toggle all button (selects / deselects) --- 
        self.toggle_frame = tk.Frame(self.right_frame)
        self.toggle_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.toggle_all_button = tk.Button(self.toggle_frame, text="Toggle All", command=self.toggle_all_classes)
        self.toggle_all_button.pack()

        # Detection result panel (scrollable)
        tk.Label(self.right_frame, text="Detections", font=("Arial", 12, "bold")).pack()
        self.text_area = tk.Text(self.right_frame, width=30, height=20, wrap=tk.WORD)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(self.right_frame, command=self.text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_area.config(yscrollcommand=scrollbar.set)

        #Threashold for warning the user
        self.threashold = 30
        self.frames = 0
        self.warnings = 0

        # Camera
        self.cap = None
        self.running = False

        self.limit_fps = False
        self.target_fps = 30
        self.frame_duration = 1.0/self.target_fps

        # Video playback variables
        self.video_cap = None
        self.video_playing = False
        self.video_paused = False
        self.total_frames = 0
        self.current_frame_num = 0
        self.video_fps = 30

        # --- class filtering --- 
        self.class_vars = {}  # --- stores checkbox values --- 
        self.current_results = None  # --- current checkbox values --- 
        self.current_image_path = None  # --- current image path --- 
        self.current_frame = None  # --- current frame --- 

    def update_class_checkboxes(self, detected_classes):
        # --- clear all checkboxes
        for widget in self.checkbox_frame.winfo_children():
            widget.destroy()
        
        self.class_vars.clear()
        
        # --- instantiate checkbox for each class --- 
        for class_name in sorted(detected_classes):
            var = tk.BooleanVar(value=True)  # --- instantiated as true --- 
            self.class_vars[class_name] = var
            
            checkbox = tk.Checkbutton(
                self.checkbox_frame, 
                text=class_name, 
                variable=var,
                command=self.on_class_filter_change
            )
            checkbox.pack(anchor="w")

    def get_visible_classes(self):
        return [class_name for class_name, var in list(self.class_vars.items()) if var.get()]

    def on_class_filter_change(self):
        visible_classes = self.get_visible_classes()
        
        # --- re-display the current image/frame with updated filtering --- 
        if self.current_image_path:
            annotated_img, _ = annotate_image(self.current_image_path, visible_classes)
            self.display_image(annotated_img)
        elif self.current_frame is not None:
            # --- dont need to do anything - will be updated in next frame cycle --- 
            pass

    def toggle_all_classes(self):
        if not self.class_vars:
            return
            
        # --- get selected --- 
        all_selected = all(var.get() for var in self.class_vars.values())
        
        # --- set to opposite state --- 
        new_state = not all_selected
        for var in self.class_vars.values():
            var.set(new_state)
        
        # --- update display --- 
        self.on_class_filter_change()


    def toggle_video_playback(self):
        if not self.video_cap:
            return
            
        if self.video_playing:
            self.video_paused = not self.video_paused
        else:
            self.video_playing = True
            self.video_paused = False
            threading.Thread(target=self.video_playback_loop, daemon=True).start()

    def stop_video(self):
        self.video_playing = False
        self.video_paused = False
        if self.video_cap:
            self.video_cap.release()
            self.video_cap = None
        
        # Disable video controls
        self.play_pause_button.config(state=tk.DISABLED)
        self.stop_video_button.config(state=tk.DISABLED)
        
        # Clear current states
        self.current_image_path = None
        self.current_frame = None

    """def seek_video(self, value):
        if not self.video_cap:
            return
        frame_num = int(value)
        self.seek_to_frame(frame_num)"""

    def seek_to_frame(self, frame_num):
        if not self.video_cap:
            return
            
        self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.video_cap.read()
        if ret:
            self.current_frame_num = frame_num
            
            # Apply filtering and display
            visible_classes = self.get_visible_classes()
            annotated_frame, results = annotate_frame(frame, visible_classes)
            
            # Update detected classes
            detected_classes = set()
            if results and results.boxes:
                for box in results.boxes:
                    cls_id = int(box.cls[0])
                    class_name = model.names[cls_id]
                    detected_classes.add(class_name)
            
            # Update checkboxes if new classes detected
            current_checkbox_classes = set(self.class_vars.keys())
            if detected_classes != current_checkbox_classes and detected_classes:
                current_states = {name: var.get() for name, var in list(self.class_vars.items())}
                self.update_class_checkboxes(detected_classes)
                for name, var in list(self.class_vars.items()):
                    if name in current_states:
                        var.set(current_states[name])
            
            self.display_image(annotated_frame)
            self.display_detections(results)

    def video_playback_loop(self):
        frame_duration = 1.0 / self.video_fps if self.video_fps > 0 else 1.0/30
        
        while self.video_playing and self.video_cap:
            if not self.video_paused:
                if self.current_frame_num >= self.total_frames - 1:
                    # End of video
                    self.video_playing = False
                    break
                
                self.seek_to_frame(self.current_frame_num + 1)
            
            time.sleep(frame_duration)

    def start_camera(self):
        if self.running:
            return
        self.stop_video()
        self.running = True
        self.cap = cv2.VideoCapture(0)
        self.stop_button.config(state=tk.NORMAL)
        self.cam_button.config(state=tk.DISABLED)
        self.current_image_path = None
        threading.Thread(target=self.camera_loop, daemon=True).start()

    def stop_camera(self):
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.stop_button.config(state=tk.DISABLED)
        self.cam_button.config(state=tk.NORMAL)

    def camera_loop(self):
        all_detected_classes = set()
        frame_count = 0#Number of frames where eyes are closed
        
        while self.running and self.cap.isOpened():
            ret, frame = self.cap.read()
            frame_start = time.perf_counter()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            self.current_frame = frame.copy()
            
            # --- get results and update detected classes --- 
            visible_classes = self.get_visible_classes()
            annotated_frame, results = annotate_frame(frame, visible_classes)
            self.current_results = results
            
            # --- collect all detected classes across frames --- 
            if results and results.boxes:
                for box in results.boxes:
                    cls_id = int(box.cls[0])
                    class_name = model.names[cls_id]
                    all_detected_classes.add(class_name)
            else:
                frame_count += 1#increment count if no eyes are detected

            if frame_count > self.threashold:
                self.warnings += 1
                #warn(self.warnings)
                #Thread
                threading.Thread(target=warn(self.warnings), daemon=False).run()
                self.frames = 0
                frame_count = 0
            
            if self.frames == 150:
                self.frames = 0
                frame_count = 0
                """Program only checks for amount of time with
                eyes closed per 5 seconds.
                Therefore frame_count resets every 150 frames (30fps)"""
            
            # ---  update checkboxes if new classes detected --- 
            current_checkbox_classes = set(self.class_vars.keys())
            if all_detected_classes != current_checkbox_classes:
                # Preserve current checkbox states
                current_states = {name: var.get() for name, var in list(self.class_vars.items())}
                self.update_class_checkboxes(all_detected_classes)
                # --- restore previous states, new classes default to True --- 
                for name, var in list(self.class_vars.items()):
                    if name in current_states:
                        var.set(current_states[name])
            
            self.display_image(annotated_frame)
            self.display_detections(results)
            delta_time = time.perf_counter() - frame_start
            sleep_time = self.frame_duration - delta_time
        
            if sleep_time > 0 and self.limit_fps:
                time.sleep(sleep_time)
            print("Frame count is: ", frame_count)
            
            self.frames += 1
            

        self.stop_camera()

    def display_image(self, bgr_img):
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(rgb_img).resize((700, 500), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img_pil)

        if not hasattr(self, 'image_id'):
            self.image_id = self.canvas.create_image(0, 0, anchor="nw", image=tk_img)
        else:
            self.canvas.itemconfig(self.image_id, image=tk_img)
        
        self.canvas.image = tk_img  # prevent GC

    def display_detections(self, result):
        self.text_area.delete(1.0, tk.END)  # Clear previous
        if not result or not result.boxes:
            self.text_area.insert(tk.END, "No detections.")
            return
        # --- add confidence ---- 
        for box in result.boxes:
            cls_id = int(box.cls[0])
            conf = float(box.conf[0])
            label = model.names[cls_id]
            self.text_area.insert(tk.END, f"{label}: {conf:.2f}\n")

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = YOLO_GUI(root)
    root.mainloop()