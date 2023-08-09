# Uptime Sheep

HTTP uptime checker: JSON target list, retries, timeouts, one-shot or loop mode.

## Config (`flock.json`)

```json
{
  "timeout_sec": 5,
  "retries": 2,
  "targets": [
    {"name": "example", "url": "https://example.com"},
    {"name": "httpbin", "url": "https://httpbin.org/status/200"}
  ]
}
```

## Usage

```bash
python3 sheep.py --once          # exit 1 if any target is down
python3 sheep.py --interval 60   # loop every 60s
```

## License

MIT
