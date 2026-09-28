# Configuration

pollwatch reads `pollwatch.toml` from the working directory, or the file given with `--config`.

## Settings

| Setting | Type | Default | Description |
| --- | --- | --- | --- |
| `url` | string | none (required) | The endpoint to poll |
| `poll_interval` | integer | `30` | Seconds between polls; at least `5` |

## Example

```toml
url = "https://status.example.com/health"
poll_interval = 60
```
