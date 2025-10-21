from time import sleep

def heart_rate(string, yolo_gui):
    while True:
        with yolo_gui.heart_state:
            if yolo_gui.heart_paused:
                yolo_gui.heart_state.wait()
            print("Checking heart rate!")
            sleep(1)