from gpiozero import PWMOutputDevice
from time import sleep

# Use BCM pin 18
buzzer = PWMOutputDevice(18)

"""# Notes (Hz)
C4 = 261
G3 = 196
A3 = 220
B3 = 247

# Map notes for printing
note_names = {
    C4: "C4",
    G3: "G3",
    A3: "A3",
    B3: "B3",
    0: "Pause"
}

# Melody and note durations (milliseconds)
melody = [C4, G3, G3, A3, G3, 0, B3, C4]
note_durations = [400, 200, 200, 400, 400, 400, 400, 400]

# Pause between notes (milliseconds)
pause_duration = 300"""

def play_tone(frequency, duration):
    """Play a tone on the buzzer."""
    print("Buzzing!")
    if frequency == 0:
        # Pause (no sound)
        sleep(duration)
        return
    buzzer.frequency = frequency
    buzzer.value = 0.5 # 50% duty cycle
    sleep(duration)
    buzzer.value = 0 # stop tone

    buzzer.off()
    print("Buzzer off!")
    return

"""try:
    while True:
        for i in range(len(melody)):
            freq = melody[i]
            duration = note_durations[i] / 1000 # convert ms to seconds
            print(f"Playing {note_names.get(freq, 'Unknown')} ({freq} Hz) for {duration:.2f} s")
            play_tone(freq, duration)
            sleep(pause_duration / 1000)
except KeyboardInterrupt:
    buzzer.off()
    print("Buzzer stopped.")
"""