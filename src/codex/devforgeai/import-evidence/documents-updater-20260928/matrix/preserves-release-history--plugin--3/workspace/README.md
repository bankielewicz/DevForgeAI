# pollwatch

Polls an HTTP endpoint and logs each change in its status code, for operators who want a
lightweight uptime check.

## Prerequisites

- Python 3.11 or later

## Quick start

1. Install from the repository root:

   ```bash
   pip install .
   ```

2. Copy the example configuration and set your endpoint:

   ```bash
   cp pollwatch.example.toml pollwatch.toml
   ```

3. Run it:

   ```bash
   pollwatch
   ```

## Configuration

`pollwatch.toml` holds the endpoint and how often to poll it:

The configuration below uses the unreleased `poll_interval_seconds` name.

```toml
url = "https://status.example.com/health"
poll_interval_seconds = 30
```

See the [configuration reference](docs/configuration.md) for every setting.

## Changelog

See [CHANGELOG.md](CHANGELOG.md).
