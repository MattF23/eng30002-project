from buzzer import play_tone
from gpiozero import RGBLED
from colorzero import Color

def warn(warnings = 1):
    """
    Function that will warn the driver of impending doom.
    Buzzes the buzzer a different amount of time based on the level of warning
    """
    #Implementation

    led = RGBLED(23, 24, 22)

    if warnings ==  1:
        led.blink(0.1, 0.1, n=3)
        play_tone(261, 0.5)
        led.off()
    elif warnings == 2:
        led.blink(0.1, 0.1, n = 3)
        play_tone(196, 1)
        led.off()
    elif warnings >= 3:
        led.blink(0.1, 0.1, n = 3)
        play_tone(220, 2)
        led.off()
    else:
        return
