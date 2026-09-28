# Configuration

pollwatch reads `pollwatch.toml` from the working directory, or the file given with `--config`.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| `url` | string | none (required) | The endpoint to poll |
| `poll_interval_seconds` | integer | `30` | Seconds between polls; at least `5` |

For the unreleased configuration change, rename `poll_interval` to `poll_interval_seconds`
in existing configuration files, keeping the same value. The old key no longer controls the
polling interval; if `poll_interval_seconds` is omitted, the interval defaults to 30 seconds.

## Example

```toml
url = "https://status.example.com/health"
poll_interval_seconds = 60
```
