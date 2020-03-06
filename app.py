import logging

from config import Config
from slate_rules_notifier.notifiers.slack import SlackFormatter, SlackHandler
from slate_rules_notifier.rules_monitor import RuleMonitor

sh = SlackHandler(Config.SLACK_WEBHOOK_URL)
sf = SlackFormatter(title="Rules Engine Monitor")
sh.setFormatter(sf)
logger = logging.getLogger(__name__)
logger.addHandler(sh)
logger.setLevel(logging.INFO)

monitor = RuleMonitor()
monitor.config.from_object(Config)


def main():
    monitor.run()


if __name__ == "__main__":
    main()
