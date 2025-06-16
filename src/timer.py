import pygame

TIME_SECOND = 1 * 1000
TIME_MINUTE = 60 * TIME_SECOND

class Timer:
    def __init__(self, wait_time: float = 0):
        self.wait_time = wait_time
        self.timer_start = 0
        self.is_counting = False
        self.is_stopped = False
        self.last_tick = 0
        self.time_passed = 0

    def start(self):
        self.is_counting = True
        self.is_stopped = False
        self.timer_start = pygame.time.get_ticks() 
        self.last_tick = self.timer_start

    def stop(self):
        self.is_counting = False
        self.is_stopped = True

    def tick(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_tick >= 1000:
            self.last_tick += 1000
            return True
        return False

    def get_time_passed(self):
        if self.is_stopped:
            return self.time_passed
        self.time_passed = pygame.time.get_ticks() - self.timer_start
        return self.time_passed
    
    def get_remains_time(self):
        return self.wait_time - self.get_time_passed()
    
    def time_is_up(self):
        is_up = self.get_time_passed() >= self.wait_time
        if is_up:
            self.is_counting = False
        return is_up

    def restart(self):
        self.stop()
        self.start()

def time_to_string(time_ms: int):
    time_seconds = time_ms // 1000
    minutes = time_seconds // 60
    seconds = time_seconds % 60
    time_string = f"{minutes:02d}:{seconds:02d}"
    return time_string
    
