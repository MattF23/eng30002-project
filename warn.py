from buzzer import play_tone

def warn(warnings = 1):
    """
    Function that will warn the driver of impending doom.
    Buzzes the buzzer a different amount of time based on the level of warning
    """
    #Implementation

    if warnings ==  1:
        play_tone(261, 500)
    elif warnings == 2:
        play_tone(196, 750)
    elif warnings >= 3:
        play_tone(220, 1000)
    else:
        return
