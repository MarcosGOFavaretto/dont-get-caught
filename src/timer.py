import pygame

class Timer:
    def __init__(self, wait_time: float):
        self.wait_time = wait_time
        self.wait_time_start = 0
        self.is_counting = False

    def start(self):
        self.is_counting = True
        self.wait_time_start = pygame.time.get_ticks()    

    def stop(self):
        self.is_counting = False
        self.wait_time_start = 0

    def get_time_passed(self):
        return pygame.time.get_ticks() - self.wait_time_start
    
    def time_is_up(self):
        return self.get_time_passed() >= self.wait_time

    def restart(self):
        self.stop()
        self.start()
    
