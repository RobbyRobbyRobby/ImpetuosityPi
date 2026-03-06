import threading
import time

class RepeatingTimer:
    """
    A timer that repeatedly executes a given function at fixed intervals.
    """
    def __init__(self, interval, function, *args, **kwargs):
        """
        :param interval: Time in seconds between function calls.
        :param function: The function to execute.
        :param args: Positional arguments for the function.
        :param kwargs: Keyword arguments for the function.
        """
        if not callable(function):
            raise ValueError("function must be callable")
        if interval <= 0:
            raise ValueError("interval must be greater than zero")

        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self._timer = None
        self._is_running = False
        self._lock = threading.Lock()

    def _run(self):
        with self._lock:
            if self._is_running:
                self.function(*self.args, **self.kwargs)
                self._schedule_next()

    def _schedule_next(self):
        self._timer = threading.Timer(self.interval, self._run)
        self._timer.daemon = True  # Allows program to exit even if timer is running
        self._timer.start()

    def start(self):
        """Start the repeating timer."""
        with self._lock:
            if not self._is_running:
                self._is_running = True
                self._schedule_next()

    def stop(self):
        """Stop the repeating timer."""
        with self._lock:
            self._is_running = False
            if self._timer:
                self._timer.cancel()



# Example usage
if __name__ == "__main__":
    def say_hello(name):
        print(f"[{time.strftime('%H:%M:%S')}] Hello, {name}!")

    timer = RepeatingTimer(2, say_hello, "Alice")  # Every 2 seconds
    timer.start()

    try:
        time.sleep(7)  # Let it run for a while
    finally:
        timer.stop()
        print("Timer stopped.")