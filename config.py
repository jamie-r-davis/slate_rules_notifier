import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    SLATE_ENDPOINT_URL = os.getenv("SLATE_ENDPOINT_URL")
    SLATE_RULES_URL = os.getenv("SLATE_RULES_URL")
    SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
    DEFAULT_THRESHOLD = int(os.getenv("DEFAULT_THRESHOLD", 240))
    QUEUE_THRESHOLDS = {
        "rule:application": 120,
        "rule:application:defer": 1440,
        "rule:person": 120,
        "rule:person:defer": 1440,
    }
