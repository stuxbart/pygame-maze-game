import time


class Clock:
    def __init__(self, init=False):
        self._system_time = time.perf_counter
        self._system_time_last = self._system_time()
        self.time = 0.0
        self._running = False
        self._initialized = False
        if init:
            self.start()

    def start(self):
        self._running = True

        if not self._initialized:
            self._system_time_last = self._system_time()
            self._initialized = True

    def stop(self):
        self._running = False

    def reset_time(self):
        self.time = 0.0

    def tick(self):
        if self._running:
            dt = self._system_time() - self._system_time_last
            self.time += dt
        self._system_time_last = self._system_time()
