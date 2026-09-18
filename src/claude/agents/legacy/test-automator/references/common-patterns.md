# Common Test Patterns

Reference documentation for test-automator subagent. Contains patterns for mocking, async testing, and exception testing.

---

## Mocking External Dependencies

### Python (unittest.mock)

```python
from unittest.mock import Mock, patch

def test_should_fetch_user_from_api():
    # Arrange
    mock_api = Mock()
    mock_api.get_user.return_value = {"id": 1, "name": "Alice"}
    service = UserService(api=mock_api)

    # Act
    user = service.get_user(user_id=1)

    # Assert
    assert user.name == "Alice"
    mock_api.get_user.assert_called_once_with(1)
```

### Patching

```python
@patch('my_module.external_api')
def test_with_patch(mock_api):
    mock_api.fetch.return_value = {"data": "value"}
    result = my_function()
    assert result == expected
```

### Context Manager

```python
def test_with_context_manager():
    with patch('my_module.dependency') as mock_dep:
        mock_dep.return_value = "mocked"
        result = function_using_dependency()
        assert result == "mocked"
```

---

### JavaScript (jest.mock)

```javascript
jest.mock('./api');
import { getUser } from './api';

test('should fetch user from API', async () => {
  // Arrange
  getUser.mockResolvedValue({ id: 1, name: 'Alice' });
  const service = new UserService();

  // Act
  const user = await service.getUser(1);

  // Assert
  expect(user.name).toBe('Alice');
  expect(getUser).toHaveBeenCalledWith(1);
});
```

### Manual Mocks

```javascript
// __mocks__/api.js
export const getUser = jest.fn();
export const saveUser = jest.fn();

// test file
jest.mock('./api');
```

### Spy Functions

```javascript
test('should call callback', () => {
  const callback = jest.fn();
  processWithCallback(data, callback);
  expect(callback).toHaveBeenCalledWith(expectedArg);
});
```

---

### C# (Moq)

```csharp
using Moq;

[Fact]
public void Should_Fetch_User_From_Api()
{
    // Arrange
    var mockApi = new Mock<IUserApi>();
    mockApi.Setup(a => a.GetUser(1))
           .Returns(new User { Id = 1, Name = "Alice" });
    var service = new UserService(mockApi.Object);

    // Act
    var user = service.GetUser(1);

    // Assert
    Assert.Equal("Alice", user.Name);
    mockApi.Verify(a => a.GetUser(1), Times.Once);
}
```

### Setup Sequences

```csharp
mockService.SetupSequence(s => s.FetchData())
    .Returns("first")
    .Returns("second")
    .Throws(new Exception("third fails"));
```

---

## Testing Async Code

### Python (pytest-asyncio)

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

### Mocking Async

```python
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_service():
    mock_client = AsyncMock()
    mock_client.fetch.return_value = {"result": "data"}

    service = AsyncService(client=mock_client)
    result = await service.process()

    assert result == {"result": "data"}
```

---

### JavaScript (async/await)

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

---

### C# (async Task)

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

### Async Setup

```csharp
[Fact]
public async Task Should_Handle_Async_Setup()
{
    // Arrange
    var mockService = new Mock<IAsyncService>();
    mockService.Setup(s => s.ProcessAsync())
               .ReturnsAsync(new Result { Success = true });

    // Act
    var result = await mockService.Object.ProcessAsync();

    // Assert
    Assert.True(result.Success);
}
```

---

## Testing Exceptions

### Python

```python
import pytest

def test_should_raise_error_for_negative_age():
    # Arrange
    user = User()

    # Act & Assert
    with pytest.raises(ValueError, match="Age cannot be negative"):
        user.set_age(-5)
```

### Validating Exception Properties

```python
def test_exception_has_correct_message():
    with pytest.raises(CustomError) as exc_info:
        raise_custom_error()

    assert exc_info.value.code == 404
    assert "not found" in str(exc_info.value)
```

---

### JavaScript

```javascript
test('should throw error for negative age', () => {
  // Arrange
  const user = new User();

  // Act & Assert
  expect(() => user.setAge(-5)).toThrow('Age cannot be negative');
});
```

### Async Exceptions

```javascript
test('should reject with specific error', async () => {
  await expect(asyncOperation()).rejects.toThrow(CustomError);
  await expect(asyncOperation()).rejects.toMatchObject({
    code: 404,
    message: expect.stringContaining('not found')
  });
});
```

---

### C#

```csharp
[Fact]
public void Should_Throw_Error_For_Negative_Age()
{
    // Arrange
    var user = new User();

    // Act & Assert
    var exception = Assert.Throws<ArgumentException>(() => user.SetAge(-5));
    Assert.Contains("Age cannot be negative", exception.Message);
}
```

### Async Exceptions

```csharp
[Fact]
public async Task Should_Throw_On_Invalid_Input()
{
    // Arrange
    var service = new ValidationService();

    // Act & Assert
    await Assert.ThrowsAsync<ValidationException>(
        async () => await service.ValidateAsync(null)
    );
}
```

---

## Best Practices Summary

### Mocking

1. **Mock at boundaries** - External services, databases, file system
2. **Don't over-mock** - Test real logic when possible
3. **Verify interactions** - Confirm mocks were called correctly
4. **Use dependency injection** - Makes mocking easier

### Async

1. **Always await** - Don't forget to await async operations
2. **Test timeouts** - Ensure async operations don't hang
3. **Test cancellation** - Verify cancellation tokens work
4. **Test failure paths** - What happens when async fails?

### Exceptions

1. **Test specific types** - Not just "any exception"
2. **Verify messages** - Exception messages should be helpful
3. **Test exception properties** - Error codes, inner exceptions
4. **Don't catch and ignore** - Always assert something
