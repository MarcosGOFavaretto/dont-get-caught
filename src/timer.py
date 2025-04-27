import pygame

class Timer:
    def __init__(self, wait_time: float):
        self.wait_time = wait_time
        self.wait_time_start = 0
        self.is_counting = False
        self.last_tick = 0

    def start(self):
        self.is_counting = True
        self.wait_time_start = pygame.time.get_ticks() 
        self.last_tick = self.wait_time_start

    def stop(self):
        self.is_counting = False
        self.wait_time_start = 0

    def tick(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_tick >= 1000:
            self.last_tick += 1000
            return True
        return False

    def get_time_passed(self):
        return pygame.time.get_ticks() - self.wait_time_start
    
    def time_is_up(self):
        return self.get_time_passed() >= self.wait_time

    def restart(self):
        self.stop()
        self.start()

def time_to_string(time_ms: int):
    time_seconds = time_ms // 1000
    minutes = time_seconds // 60
    seconds = time_seconds % 60
    time_string = f"{minutes:02d}:{seconds:02d}"
    return time_string
    
