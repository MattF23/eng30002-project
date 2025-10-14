from gpiozero import RGBLED, PWMOutputDevice
from time import sleep

def warn(warnings = 1, duration = 0.2, frequency = 1000, duty = 0.5):
    """
    Function that will warn the driver of impending doom.
    Buzzes the buzzer a different amount of time based on the level of warning
    """
    #Implementation

    led = RGBLED(23, 24, 25)
    buzzer = PWMOutputDevice(21)

    if warnings ==  1:
        led.color('yellow')
        led.blink(on_time = 0.5, off_time = 0.5)
        buzzer.frequency = frequency
        buzzer.value = duty
        sleep(duration)
        buzzer.value = 0
        led.off()
    elif warnings == 2:
        led.color('orange')
        led.blink(on_time = 0.3, off_time = 0.3)
        buzzer.frequency = 1200
        buzzer.value = 0.6
        sleep(0.15)
        buzzer.vale = 0
        led.off()
    elif warnings >= 3:
        led.color('red')
        led.blink(on_time = 0.1, off_time = 0.1)
        buzzer.frequency = 1600
        buzzer.value = 1.0
        sleep(0.2)
        buzzer.value = 0
        led.off()
    else:
        return
