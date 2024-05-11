from typing import TypeVar, Generic, Callable, ParamSpec

K = TypeVar("K", int, str)
I = ParamSpec("I")
O = TypeVar("O")


class EventListener(Generic[K, I, O]):
    def __init__(self):
        self.events: dict[K, list[Callable[I, O]]] = {}

    def on(self, event_type: K, callback: Callable[I, O]):
        if event_type not in self.events:
            self.events[event_type] = []
        self.events[event_type].append(callback)

    def once(self, event_type: K, callback: Callable[I, O]):
        def once_callback(*args: I.args, **kwargs: I.kwargs):
            callback(*args, **kwargs)
            self.off(event_type, once_callback)

        self.on(event_type, once_callback)

    def off(self, event_type: K, callback: Callable[I, O]):
        if event_type in self.events:
            self.events[event_type].remove(callback)

    def emit(self, event_type: K, *args: I.args, **kwargs: I.kwargs):
        if event_type in self.events:
            for callback in self.events[event_type]:
                callback(*args, **kwargs)
