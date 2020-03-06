import logging

import requests


class SlackHandler(logging.Handler):
    """Logging handler to post to Slack webhook URL"""

    def __init__(self, hook_url):
        super().__init__()
        self._hook_url = hook_url
        self.formatter = SimpleSlackFormatter()

    @property
    def hook_url(self):
        return self._hook_url

    def emit(self, record):
        """
        Submit the record with a POST request
        """
        try:
            slack_data = self.format(record)
            requests.post(self.hook_url, json=slack_data)
        except Exception:
            self.handleError(record)

    def filter(self, record):
        """
        Disable the logger if hook_url isn't defined,
        we don't want to do it in all environments.
        """
        if not self.hook_url:
            return 0
        return super().filter(record)


class SlackLogFilter(logging.Filter):
    """
    Logging filter to decide when logging to Slack is requested, using
    the `extra` kwargs:

        `logger.info("...", extra={'notify_slack': True})`
    """

    def filter(self, record):
        return getattr(record, "notify_slack", False)


class SimpleSlackFormatter(logging.Formatter):
    """Basic formatter without styling"""

    def format(self, record):
        return {"text": record.getMessage()}


class SlackFormatter(logging.Formatter):
    """
    Formatter for Slack messages. Setting the `title` will add a
    heading to the messages.
    """

    def __init__(self, title=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = title

    def format(self, record):
        """
        Format message content, timestamp when it was logged, and a
        colored border depending on the severity of the message
        """
        print(record)
        fields = getattr(record, "fields", [])
        actions = getattr(record, "actions", [])
        ret = {
            "ts": record.created,
            "text": record.getMessage(),
            "title": self.title,
            "fields": fields,
            "actions": actions,
        }
        try:
            loglevel_color = {
                "INFO": "good",
                "WARNING": "warning",
                "ERROR": "#E91E63",
                "CRITICAL": "danger",
            }
            ret["color"] = loglevel_color[record.levelname]
        except KeyError:
            pass
        return {"attachments": [ret]}
