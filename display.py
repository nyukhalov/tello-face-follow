import cv2
import pygame
from pygame.locals import DOUBLEBUF

class Display2D(object):
    def __init__(self):
        pass

    # abstract
    def paint(self, img):
        pass

    # abstract
    def dispose(self):
        pass

class Cv2Display2D(Display2D):
    def __init__(self, win_title='Main'):
        self.win_title = win_title

    def paint(self, img):
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        cv2.imshow(self.win_title, img)
        cv2.waitKey(1)

    def dispose(self):
        cv2.destroyAllWindows()

class PygameDisplay(Display2D):
    def __init__(self, W, H):
        pygame.init()
        self.screen = pygame.display.set_mode((W,H), DOUBLEBUF)
        self.surface = pygame.Surface(self.screen.get_size()).convert()

    def paint(self, img):
        for event in pygame.event.get():
            pass

        pygame.surfarray.blit_array(self.surface, img.swapaxes(0,1)[:, :, [0,1,2]])
        self.screen.blit(self.surface, (0,0))
        pygame.display.flip()
