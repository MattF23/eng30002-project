from time import sleep
from colorzero import Color

def warn(led, buzzer, warnings = 1, frequency = 1000, duty = 0.5):
    """
    Function that will warn the driver of impending doom.
    Buzzes the buzzer a different amount of time based on the level of warning
    """
    #Implementation
    if warnings ==  1:
        led.color = Color('yellow')
        led.blink(on_time = 0.05, off_time = 0.05)
        buzzer.frequency = frequency
        buzzer.value = duty
        sleep(0.2)
        buzzer.value = 0
        led.off()
    elif warnings == 2:
        led.color = Color('orange')
        led.blink(on_time = 0.1, off_time = 0.1)
        buzzer.frequency = 1200
        buzzer.value = 0.6
        sleep(0.4)
        buzzer.value = 0
        led.off()
    elif warnings >= 3:
        led.color = Color('red')
        led.blink(on_time = 0.1, off_time = 0.1)
        buzzer.frequency = 1600
        buzzer.value = 1.0
        sleep(0.6)
        buzzer.value = 0
        led.off()
    else:
        return
