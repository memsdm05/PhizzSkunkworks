import time
import asyncio
import websockets

class PingStopwatch():
    def __init__(self):
        self.milli = lambda: int(round(time.time() * 1000))
        self.elapsed = 0
        self._start = 0
        self._stop = 0

    def start(self):
        self._start = self.milli()

    def stop(self):
        self._stop = self.milli()
        self.elapsed = self._stop = self._start
        self._stop = 0
        self._start = 0

