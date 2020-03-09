import logging
from random import choices, randint
from typing import List

import requests

from .logging import create_logger


class Config(dict):
    def __init__(self, defaults: dict = None):
        super().__init__(defaults or {})

    def from_object(self, obj):
        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)


class RulesMonitor:
    def __init__(self, name, config=None, debug=False):
        self.name = name
        self.debug = debug
        self.config = Config()
        if config:
            self.config.from_object(config)
        self.logger = create_logger(self)

    def fetch_queues(self):
        url = self.config.get("SLATE_ENDPOINT_URL")
        response = requests.get(url)
        response.raise_for_status()
        queues = response.json()["row"]
        self.logger.debug(f"Queues retrieved: {queues}")
        return queues

    def filter_queues_by_threshold(self, queues: List[dict]) -> List[dict]:
        thresholds = self.config.get("QUEUE_THRESHOLDS")
        default_threshold = self.config.get("DEFAULT_THRESHOLD")
        filtered_queues = []
        for queue in queues:
            queue_threshold = thresholds.get(queue["key"], default_threshold)
            if int(queue["staleness"]) >= queue_threshold:
                filtered_queues.append(queue)
        return filtered_queues

    def send_notification(self, exceeded_queues: List[dict]):
        emoji_options = "🔥💩🦄💣🙀🛬🚨🚧🚒💥😿"
        emoji = "".join(choices(emoji_options, k=randint(3, 6)))
        msg = f"Rules have queued past their minimum threshold!\n\n{emoji}"
        fields = []
        for row in exceeded_queues:
            fields.append(
                {
                    "title": row["category"],
                    "value": f"{int(row['records']):,} records ({int(row['staleness']):,} min)",
                    "short": True,
                }
            )
        actions = [
            {
                "type": "button",
                "text": "View Rules",
                "url": self.config.get("SLATE_RULES_URL"),
                "style": "danger",
            }
        ]
        self.logger.debug(f"Slack msg: {msg}, fields={fields}, actions={actions}")
        self.logger.critical(msg, extra={"fields": fields, "actions": actions})

    def run(self):
        queues = self.fetch_queues()
        exceeded_queues = self.filter_queues_by_threshold(queues)
        if exceeded_queues:
            self.send_notification(exceeded_queues)
        else:
            self.logger.debug("No queues have exceeded their thresholds")
