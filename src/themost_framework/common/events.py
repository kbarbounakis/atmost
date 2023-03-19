from typing import Callable


class SyncEventHandler:
    def __init__(self, handler):
        self.handler = handler

    def execute(self, *args):
        self.handler(*args)

class OnceSyncEventHandler(SyncEventHandler):
    def __init__(self, handler):
        self.fired = False
        super().__init__(handler)

    def execute(self, *args):
        if self.fired:
            return
        super().execute(*args)
        self.fired = True

class SyncSubscription:
    def __init__(self, emitter, handler):
        self.__emitter__ = emitter
        self.__handler__ = handler

    def unsubscribe(self):
        self.__emitter__.unsubscribe(self.__handler__)

class SyncSeriesEventEmitter:

    def __init__(self):
        self.__handlers__ = []
    
    def subscribe(self, handler):
        """Appends an event handler and waits for event
        Parameters:
                    handler (Callable): An event handler to include
        Returns: 
                subscription (SyncSubscription): An object which represents an event subscription for later use
        """
        handle = SyncEventHandler(handler)
        self.__handlers__.append(handle)
        return SyncSubscription(self, handle)

    def subscribe_once(self, handler):
        """Appends an event handler and waits for event
        Parameters:
                    handler (Callable): An event handler to include
        Returns: 
                subscription (SyncSubscription): An object which represents an event subscription for later use
        """
        handle = OnceSyncEventHandler(handler)
        self.__handlers__.append(handle)
        return SyncSubscription(self, handle)
    
    def unsubscribe(self, handler):
        """Removes a previously added event handler

        Args:
            handler (SyncEventHandler): An event handler to remove
        """
        self.__handlers__.remove(handler)

    def emit(self, *args):
        for handler in self.__handlers__:
            handler.execute(*args)


