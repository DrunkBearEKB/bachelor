from typing import Set

from bachelor_core.common.http.requests import http_get

from bachelor_core.application.plugins.secrets import get_value_from_secrets
from base_processor import BaseProcessor
from scheduler_wrapper.task import Task


class TelegramNotifyProcessor(BaseProcessor):
    def _process_task(self, task: Task):
        bot_token = get_value_from_secrets(self.config.get("token_secret"))
        bot_chat_id = get_value_from_secrets(self.config.get("chat_id_secret"))
        text = task.payload.get("text", 5)

        url = (
            f"https://api.telegram.org/bot{bot_token}/"
            f"sendMessage?chat_id={bot_chat_id}&parse_mode=Markdown&text={text}"
        )
        http_get(url)

    def supported_topics(self) -> Set[str]:
        return {"telegram_notify"}
