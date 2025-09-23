import pygame.mixer as mixer
import pygame.time
import subprocess

def warn(warnings):
    """
    Function that will warn the driver of impending doom.
    Plays a different sound file based on the amount of warning

    It first sets the approapriate volume.
    Then plays an audio file that corresponds to the urgency of warning.
    """

    mixer.init()

    if warnings == 1:
        #set volume
        subprocess.Popen("amixer scontrols && amixer sset 'Master 30%'", shell = True)

        sound = mixer.Sound("audio/warning1.mp3")
        playing = sound.play()

        while(playing.get_busy()):#While loop needed to stop script from terminating before the audio file has finished playing!
            pygame.time.delay(100)

    elif warnings == 2:
        #set volume
        subprocess.Popen("amixer scontrols && amixer sset 'Master 60%'", shell = True)

        sound = mixer.Sound("audio/warning2.mp3")
        playing = sound.play()

        while(playing.get_busy()):
            pygame.time.delay(100)

    else:
        #set volume
        subprocess.Popen("amixer scontrols && amixer sset 'Master 90%'", shell = True)

        sound = mixer.Sound("audio/warning3.mp3")
        playing = sound.play()

        while(playing.get_busy()):
            pygame.time.delay(100)