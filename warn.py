import pygame.mixer as mixer
import playsound
import subprocess

def warn(warnings = 1):
    """
    Function that will warn the driver of impending doom.
    Plays a different sound file based on the amount of warning

    It first sets the approapriate volume.
    Then plays an audio file that corresponds to the urgency of warning.
    """

    mixer.init()

    if warnings == 1:
        #set volume
        #subprocess.Popen("amixer scontrols && amixer sset 'Master 30%'", shell = True)

        playsound.playsound('audio/warning1.mp3', False)

    elif warnings == 2:
        #set volume
        #subprocess.Popen("amixer scontrols && amixer sset 'Master 60%'", shell = True)

        playsound.playsound('audio/warning2.mp3', False)

    else:
        #set volume
        #subprocess.Popen("amixer scontrols && amixer sset 'Master 90%'", shell = True)

        playsound.playsound('audio/warning3.mp3', False)
