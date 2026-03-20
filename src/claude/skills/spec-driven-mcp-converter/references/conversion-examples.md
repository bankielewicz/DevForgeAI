# MCP-CLI Converter: Concrete Examples

Real-world examples of MCPs being converted to CLIs with auto-generated skills.

## Example 1: Puppeteer MCP → State-Based CLI

### The MCP (Input)

```python
@mcp.tool()
async def navigate(url: str) -> dict:
    """Navigate browser to URL."""
    return {"url": url, "loaded": True}

@mcp.tool()
async def screenshot(selector: str = None) -> bytes:
    """Take screenshot of page or element."""
    return await browser.screenshot()

@mcp.tool()
async def click(selector: str) -> dict:
    """Click element."""
    return {"clicked": selector}

@mcp.tool()
async def extract_text(selector: str) -> str:
    """Extract text content."""
    return await page.text_content(selector)
```

### Analysis Output

```json
{
  "mcp_type": "puppeteer-mcp",
  "detected_pattern": "state-based",
  "confidence": 0.98,
  "state_management": {
    "stateful": true,
    "session_required": true,
    "state_keywords": ["browser", "page", "navigate", "click"]
  }
}
```

### Generated CLI

```bash
SESSION=$(python cli.py session create --name "scrape-job")
python cli.py navigate --session $SESSION --url "https://example.com"
python cli.py screenshot --session $SESSION --selector "body" --format base64
python cli.py extract-text --session $SESSION --selector "div.content" --format json
python cli.py session destroy --session $SESSION
```

---

## Example 2: OpenWeather API → API Wrapper CLI

### The MCP (Input)

```typescript
@tool()
async function getForecast(location: string, days: number = 5): Promise<WeatherForecast> {
  return weatherData;
}

@tool()
async function getCurrentWeather(location: string): Promise<CurrentWeather> {
  return currentWeatherData;
}

@tool()
async function searchCities(query: string): Promise<City[]> {
  return citiesMatchingQuery;
}
```

### Analysis Output

```json
{
  "mcp_type": "openweather-mcp",
  "detected_pattern": "api-wrapper",
  "confidence": 0.97,
  "state_management": {
    "stateful": false,
    "session_required": false
  }
}
```

### Generated CLI

```bash
python cli.py get-forecast --location "Seattle" --days 5 --format json
python cli.py get-current-weather --location "Seattle" --format json
python cli.py search-cities --query "San" --format json
```

---

## Example 3: PostgreSQL MCP → State-Based CLI

### The MCP (Input)

```python
@mcp.tool()
async def connect(host: str, port: int, username: str, password: str, database: str) -> dict:
    """Connect to PostgreSQL."""

@mcp.tool()
async def execute(sql: str) -> list:
    """Execute SQL query (requires active connection)."""

@mcp.tool()
async def begin_transaction() -> dict:
    """Start transaction."""

@mcp.tool()
async def commit() -> dict:
    """Commit transaction."""
```

### Analysis Output

```json
{
  "mcp_type": "postgres-mcp",
  "detected_pattern": "state-based",
  "confidence": 0.99,
  "state_management": {
    "stateful": true,
    "session_required": true,
    "state_keywords": ["connect", "transaction", "commit", "rollback"]
  }
}
```

### Generated CLI

```bash
CONN=$(python cli.py session create --name "data-load")
python cli.py connect --session $CONN --host localhost --port 5432 --username user --password pass --database mydb
python cli.py begin-transaction --session $CONN
python cli.py execute --session $CONN --sql "INSERT INTO users ..."
python cli.py commit --session $CONN
python cli.py session destroy --session $CONN
```

---

## Example 4: Custom MCP → Custom Adapter

For MCPs with caching, streaming, or hybrid patterns:

```python
class MyServiceAdapter:
    def __init__(self):
        self.cache = {}

    def execute(self, command, args):
        if command == "search":
            return self._search_with_cache(args)
        elif command == "stream-results":
            return self._stream_results(args)
```

```bash
/convert-mcp myservice --pattern custom --adapter-script ./my_adapter.py
python cli.py search --query "data" --format json
python cli.py cache-status
```

---

## Summary

| Pattern | Example | Confidence | Key Feature |
|---------|---------|------------|-------------|
| API Wrapper | OpenWeather | 0.97 | Stateless, direct mapping |
| State-Based | Puppeteer | 0.98 | Session lifecycle |
| State-Based | PostgreSQL | 0.99 | Connection + transactions |
| Custom | MyService | N/A | Caching + streaming |
