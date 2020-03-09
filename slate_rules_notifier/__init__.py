from .rules_monitor import RulesMonitor
from config import Config


def create_app(debug=False):
    monitor = RulesMonitor(__name__, config=Config, debug=debug)
    monitor.config.from_object(Config)
    if debug:
        monitor.config["QUEUE_THRESHOLDS"] = {}
        monitor.config["DEFAULT_THRESHOLD"] = 1
    return monitor
