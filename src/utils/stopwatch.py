import time


class Stopwatch:
    def __init__(self):
        self.running = False
        self._start_time = None
        self._elapsed_time = 0

    def start(self):
        if not self.running:
            self._start_time = time.time()
            self.running = True

    def stop(self):
        if self.running:
            end_time = time.time()
            self._elapsed_time += end_time - self._start_time
            self.running = False

    def reset(self):
        self._start_time = None
        self.running = False
        self._elapsed_time = 0

    def get_time(self):
        if self.running:
            end_time = time.time()
            return self._elapsed_time + end_time - self._start_time
        else:
            return self._elapsed_time

    def get_time_str(self):
        total_seconds = int(self.get_time())
        minutes, seconds = divmod(total_seconds, 60)
        tenths = int(10 * (self.get_time() - total_seconds))
        return f"{minutes}:{seconds:02}.{tenths:01}"

    def get_start_time(self):
        return self._start_time

    def get_start_time_str(self):
        return time.strftime("%I:%M:%S %p", time.localtime(self._start_time))


def main():
    # Usage:
    stopwatch = Stopwatch()
    stopwatch.start()
    # Do something...
    stopwatch.stop()
    stopwatch.reset()


if __name__ == "__main__":
    main()
