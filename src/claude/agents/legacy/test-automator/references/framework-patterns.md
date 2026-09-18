# Framework-Specific Test Patterns

Reference documentation for test-automator subagent. Contains language-specific patterns for Python/pytest, JavaScript/Jest, and C#/xUnit.

---

## Python (pytest)

### Basic Test Structure

```python
import pytest
from my_module import Calculator

@pytest.fixture
def calculator():
    """Fixture for test setup"""
    return Calculator()

def test_should_add_positive_numbers(calculator):
    # Arrange
    a, b = 5, 3

    # Act
    result = calculator.add(a, b)

    # Assert
    assert result == 8

@pytest.mark.parametrize("a,b,expected", [
    (5, 3, 8),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_should_add_various_inputs(calculator, a, b, expected):
    assert calculator.add(a, b) == expected
```

### Fixtures

```python
@pytest.fixture
def db_connection():
    """Setup and teardown database connection"""
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def expensive_resource():
    """Share resource across module tests"""
    return setup_expensive_resource()
```

### Markers

```python
@pytest.mark.slow
def test_slow_operation():
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

@pytest.mark.xfail
def test_known_failure():
    pass
```

### Async Testing (pytest-asyncio)

```python
import pytest

@pytest.mark.asyncio
async def test_should_fetch_data_asynchronously():
    # Arrange
    fetcher = AsyncDataFetcher()

    # Act
    data = await fetcher.fetch(url="https://api.example.com")

    # Assert
    assert data is not None
```

### Coverage Command

```bash
pytest --cov=src --cov-report=term --cov-report=html
```

---

## JavaScript (Jest)

### Basic Test Structure

```javascript
describe('Calculator', () => {
  let calculator;

  beforeEach(() => {
    calculator = new Calculator();
  });

  test('should add positive numbers', () => {
    // Arrange
    const a = 5, b = 3;

    // Act
    const result = calculator.add(a, b);

    // Assert
    expect(result).toBe(8);
  });

  test.each([
    [5, 3, 8],
    [-1, 1, 0],
    [0, 0, 0],
  ])('should add %i + %i = %i', (a, b, expected) => {
    expect(calculator.add(a, b)).toBe(expected);
  });
});
```

### Setup and Teardown

```javascript
describe('Database tests', () => {
  let connection;

  beforeAll(async () => {
    connection = await createConnection();
  });

  afterAll(async () => {
    await connection.close();
  });

  beforeEach(() => {
    // Reset state before each test
  });
});
```

### Async Testing

```javascript
test('should fetch data asynchronously', async () => {
  // Arrange
  const fetcher = new AsyncDataFetcher();

  // Act
  const data = await fetcher.fetch('https://api.example.com');

  // Assert
  expect(data).not.toBeNull();
});
```

### Testing Promises

```javascript
test('should resolve with data', () => {
  return fetchData().then(data => {
    expect(data).toBeDefined();
  });
});

test('should reject with error', async () => {
  await expect(fetchInvalidData()).rejects.toThrow('Invalid');
});
```

### Coverage Command

```bash
jest --coverage
```

---

## C# (xUnit)

### Basic Test Structure

```csharp
using Xunit;

public class CalculatorTests
{
    private readonly Calculator _calculator;

    public CalculatorTests()
    {
        _calculator = new Calculator();
    }

    [Fact]
    public void Should_Add_Positive_Numbers()
    {
        // Arrange
        int a = 5, b = 3;

        // Act
        int result = _calculator.Add(a, b);

        // Assert
        Assert.Equal(8, result);
    }

    [Theory]
    [InlineData(5, 3, 8)]
    [InlineData(-1, 1, 0)]
    [InlineData(0, 0, 0)]
    public void Should_Add_Various_Inputs(int a, int b, int expected)
    {
        Assert.Equal(expected, _calculator.Add(a, b));
    }
}
```

### Fixtures (IClassFixture)

```csharp
public class DatabaseFixture : IDisposable
{
    public DbConnection Connection { get; }

    public DatabaseFixture()
    {
        Connection = CreateConnection();
    }

    public void Dispose()
    {
        Connection?.Close();
    }
}

public class DatabaseTests : IClassFixture<DatabaseFixture>
{
    private readonly DatabaseFixture _fixture;

    public DatabaseTests(DatabaseFixture fixture)
    {
        _fixture = fixture;
    }

    [Fact]
    public void Should_Query_Database()
    {
        var result = _fixture.Connection.Query("SELECT 1");
        Assert.NotNull(result);
    }
}
```

### Async Testing

```csharp
[Fact]
public async Task Should_Fetch_Data_Asynchronously()
{
    // Arrange
    var fetcher = new AsyncDataFetcher();

    // Act
    var data = await fetcher.FetchAsync("https://api.example.com");

    // Assert
    Assert.NotNull(data);
}
```

### Skip and Traits

```csharp
[Fact(Skip = "Not implemented yet")]
public void Should_Handle_Future_Feature()
{
}

[Trait("Category", "Integration")]
[Fact]
public void Should_Connect_To_External_Service()
{
}
```

### Coverage Command

```bash
dotnet test --collect:"XPlat Code Coverage"
```

---

## Test Naming Conventions

All frameworks should follow the pattern:

```
test_should_[expected_behavior]_when_[condition]
```

### Examples:

| Framework | Test Name |
|-----------|-----------|
| Python | `test_should_return_empty_list_when_cart_is_empty` |
| JavaScript | `'should return empty list when cart is empty'` |
| C# | `Should_Return_Empty_List_When_Cart_Is_Empty` |

---

## AAA Pattern (All Frameworks)

```
def/function/public test():
    # Arrange: Set up test preconditions
    sut = SystemUnderTest()

    # Act: Execute the behavior being tested
    result = sut.do_something()

    # Assert: Verify the outcome
    assert result == expected_value
```

---

## Test Pyramid (All Frameworks)

```
       /\
      /E2E\      10% - Critical user paths only
     /------\
    /Integr.\   20% - Component interactions
   /----------\
  /   Unit    \ 70% - Individual functions/methods
 /--------------\
```

**Distribution Guidelines:**
- Unit tests: Fast, isolated, abundant
- Integration tests: Medium speed, component interactions
- E2E tests: Slow, full stack, critical paths only
