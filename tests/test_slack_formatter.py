import logging

import pytest

from slate_rules_notifier.notifiers.slack import SlackFormatter


class CustomLogRecord(logging.LogRecord):
    def __init__(
        self,
        level,
        msg,
        name="",
        pathname="",
        lineno="",
        args=(),
        exc_info=None,
        func=None,
        sinfo=None,
        extra=None,
    ):
        super().__init__(
            name, level, pathname, lineno, msg, args, exc_info, func, sinfo
        )
        if extra is not None:
            for k in extra:
                setattr(self, k, extra[k])


@pytest.fixture()
def slack_formatter():
    return SlackFormatter(title="Test Slack Formatter")


def test_slack_formatter(slack_formatter):
    record = CustomLogRecord(level=logging.CRITICAL, msg="Test msg")
    r = slack_formatter.format(record)
    print(r)
    assert "attachments" in r
    msg = r["attachments"][0]
    assert msg["text"] == "Test msg"
    assert msg["title"] == slack_formatter.title
    assert msg["fields"] == []
    assert msg["actions"] == []


def test_slack_formatter_extra_fields(slack_formatter):
    """Test to ensure that `fields` in extra parameter are properly encoded for Slack"""
    fields = [{"title": "Field 1", "value": "10 records (15 min)", "short": True}]
    record = CustomLogRecord(
        level=logging.CRITICAL, msg="Test msg", extra={"fields": fields}
    )
    result = slack_formatter.format(record)
    assert result["attachments"][0]["fields"] == fields
