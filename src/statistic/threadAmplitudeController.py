from concurrent.futures import ThreadPoolExecutor
from amplitude import Amplitude, BaseEvent

class ThreadAmplitudeController:
    def __init__(self, amplitude_api_key):
        self.client = Amplitude(amplitude_api_key)
        self.executor = ThreadPoolExecutor(max_workers=1)

    def _track_event(self, event_type, user_id):
        event = BaseEvent(event_type, user_id)
        res = self.client.track(event)

    def add_event(self, event_type, user_id):
        self.executor.submit(lambda: self._track_event(event_type, user_id))