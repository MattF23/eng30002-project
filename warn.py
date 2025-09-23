import pygame.mixer as mixer
import pygame.time

def warn(warnings):
    """
    Function that will warn the driver of impending doom.
    Plays a different sound file based on the amount of warning
    """

    mixer.init()

    if warnings == 1:
        sound = mixer.Sound("path/to/file")
        playing = sound.play()

        while(playing.get_busy()):
            pygame.time.delay(100)

    elif warnings == 2:
        sound = mixer.Sound("path/to/file")
        playing = sound.play()

        while(playing.get_busy()):
            pygame.time.delay(100)

    else:
        sound = mixer.Sound("path/to/file")
        playing = sound.play()

        while(playing.get_busy()):
            pygame.time.delay(100)