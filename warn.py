from buzzer import play_tone

def warn(warnings = 1):
    """
    Function that will warn the driver of impending doom.
    Buzzes the buzzer a different amount of time based on the level of warning
    """
    #Implementation

    if warnings ==  1:
        play_tone()

    elif warnings == 2:
        play_tone()
        play_tone()

    else:
        play_tone()
        play_tone()
        play_tone()
