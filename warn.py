#from buzzer import play_tone
from gpiozero import PWMOutputDevice
from time import sleep

def warn(warnings = 1):
    """
    Function that will warn the driver of impending doom.
    Buzzes the buzzer a different amount of time based on the level of warning
    """
    #Implementation

    def play_tone(frequency, duration):
        buzzer = PWMOutputDevice(18)

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

    if warnings ==  1:
        play_tone(261, 500)
    elif warnings == 2:
        play_tone(196, 750)
    elif warnings >= 3:
        play_tone(220, 1000)
    else:
        return
