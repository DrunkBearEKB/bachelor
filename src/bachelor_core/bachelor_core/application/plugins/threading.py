import threading
from typing import Dict, Any, Callable, Iterable

from bachelor_core.application.base_plugin import BasePlugin
from bachelor_core.application.application import Application


class ThreadingPlugin(BasePlugin):
    """
    Плагин для работы с потоками в приложении
    """

    NAME = "threading_plugin"
    PLUGIN_INSTALL = [
        "start_new_thread",
    ]

    def __init__(self, app: Application, config: Dict[str, Any]):
        super().__init__(app, config)

    def start_new_thread(
        self,
        target: Callable,
        args: Iterable[Any],
        kwargs
    ) -> threading.Thread:
        self.log_info("initializing new thread: started")
        try:
            thread = threading.Thread(target=target, args=args, kwargs=kwargs)
            thread.start()
            self.log_info("initializing new thread: finished", thread_name=thread.name)
            return thread
        except Exception as e:
            self.log_error("initializing new thread: failed", error=e)
            raise
