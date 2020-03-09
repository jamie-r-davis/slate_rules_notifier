import logging
import sys

from slate_rules_notifier.notifiers.slack import SlackFormatter, SlackHandler

loggers = {}


def create_logger(app):
    global loggers

    if loggers.get(app.name):
        return loggers.get(app.name)
    logger = logging.getLogger(app.name)

    if app.debug:
        logger.setLevel(logging.DEBUG)
    slack_handler = SlackHandler(app.config.get("SLACK_WEBHOOK_URL"))
    slack_handler.setFormatter(SlackFormatter("Rules Engine Monitor"))
    slack_handler.setLevel(logging.CRITICAL)
    logger.addHandler(slack_handler)

    # stream_handler = logging.StreamHandler(sys.stdout)
    # stream_handler.setLevel(logging.DEBUG)
    # logger.addHandler(stream_handler)

    loggers.update(dict(name=logger))

    return logger
