import dataclasses
import logging
from abc import ABC
from typing import List, Union


@dataclasses.dataclass
class EventTypes:
    BEFORE_SETUP = "on_before_setup"
    AFTER_SETUP = "on_after_setup"
    BEFORE_DECODE_REQUEST = "on_before_decode_request"
    AFTER_DECODE_REQUEST = "on_after_decode_request"
    BEFORE_ENCODE_RESPONSE = "on_before_encode_response"
    AFTER_ENCODE_RESPONSE = "on_after_encode_response"
    BEFORE_PREDICT = "on_before_predict"
    AFTER_PREDICT = "on_after_predict"
    BEFORE_SERVER_REGISTER = "on_before_server_register"
    AFTER_SERVER_REGISTER = "on_after_server_register"


class Callback(ABC):
    def on_before_setup(self, *args, **kwargs):
        """Called before setup is started."""

    def on_after_setup(self, *args, **kwargs):
        """Called after setup is completed."""

    def on_before_decode_request(self, *args, **kwargs):
        """Called before request decoding is started."""

    def on_after_decode_request(self, *args, **kwargs):
        """Called after request decoding is completed."""

    def on_before_encode_response(self, *args, **kwargs):
        """Called before response encoding is started."""

    def on_after_encode_response(self, *args, **kwargs):
        """Called after response encoding is completed."""

    def on_before_predict(self, *args, **kwargs):
        """Called before prediction is started."""

    def on_after_predict(self, *args, **kwargs):
        """Called after prediction is completed."""

    def on_before_server_register(self, *args, **kwargs):
        """Called before LitServer endpoint setup is started."""

    def on_after_server_register(self, *args, **kwargs):
        """Called after LitServer endpoint setup is completed."""


class CallbackRunner:
    def __init__(self):
        self._callbacks = []

    def add_callbacks(self, callbacks: Union[Callback, List[Callback]]):
        if isinstance(callbacks, list):
            self._callbacks.extend(callbacks)
        else:
            self._callbacks.append(callbacks)

    def trigger_event(self, event_name, *args, **kwargs):
        """Triggers an event, invoking all registered callbacks for that event."""
        if not self._callbacks:
            return
        for callback in self._callbacks:
            try:
                getattr(callback, event_name)(*args, **kwargs)
            except Exception:
                # Handle exceptions to prevent one callback from disrupting others
                logging.exception(f"Error in callback '{callback}' during event '{event_name}'")


class NoopCallback(Callback):
    """This callback does nothing."""
