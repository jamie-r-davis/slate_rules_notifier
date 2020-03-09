# Slate Rules Notifier

A simple app that will send Slack notifications if rule queues exceed pre-defined thresholds.


## Configuration

Configuration can be handled by updating `config.py` or by setting environment variables according to the values in `config.py`.

## Usage

Intended usage is:

```bash
python app.py
```

This will retrieve queue information from `SLATE_ENDPOINT_URL`. If any queues exceed the configured thresholds, a slack message will be emitted to the `SLACK_WEBHOOK_URL` endpoint.